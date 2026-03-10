#!/usr/bin/env python3
"""
Test script to verify the gateway is working.
Run this after starting the gateway server with: python gateway.py
"""

import requests
import sys
import time


def test_gateway():
    base_url = "http://localhost:8000"
    
    print("Testing MyOpenClaw Python Gateway...\n")
    
    # Test health endpoint
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        print("✓ Health check passed\n")
    except Exception as e:
        print(f"✗ Health check failed: {e}\n")
        return False
    
    # Test sending a message
    print("2. Testing message endpoint...")
    try:
        response = requests.post(
            f"{base_url}/message",
            json={
                "message": "Hello! Can you tell me what 2+2 equals?",
                "channel": "test",
                "account_id": "test_user_123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "response" in data
        print(f"✓ Message sent successfully")
        print(f"  Agent ID: {data['agent_id']}")
        print(f"  Session Key: {data['session_key']}")
        print(f"  Response: {data['response'][:100]}...\n")
    except Exception as e:
        print(f"✗ Message test failed: {e}\n")
        return False
    
    # Test conversation continuity
    print("3. Testing conversation continuity...")
    try:
        response = requests.post(
            f"{base_url}/message",
            json={
                "message": "What was my previous question?",
                "channel": "test",
                "account_id": "test_user_123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        print(f"✓ Conversation continued successfully")
        print(f"  Response: {data['response'][:100]}...\n")
    except Exception as e:
        print(f"✗ Conversation test failed: {e}\n")
        return False
    
    # Test sessions endpoint
    print("4. Testing sessions endpoint...")
    try:
        response = requests.get(f"{base_url}/sessions")
        assert response.status_code == 200
        sessions = response.json()["sessions"]
        print(f"✓ Found {len(sessions)} active session(s)")
        for session in sessions:
            print(f"  - {session['key']}: {session['message_count']} messages\n")
    except Exception as e:
        print(f"✗ Sessions test failed: {e}\n")
        return False
    
    print("✓ All tests passed!")
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("Make sure the gateway is running: python gateway.py")
    print("=" * 60)
    print()
    
    time.sleep(1)
    
    success = test_gateway()
    sys.exit(0 if success else 1)
