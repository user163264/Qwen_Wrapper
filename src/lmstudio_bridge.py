#!/usr/bin/env python3
"""
LMStudio Bridge for Qwen Filesystem Access
This script handles function calls from LMStudio and routes them to the filesystem handler.
"""

import sys
import json
from filesystem_handler import handle_function_call

def main():
    """
    Main function to handle LMStudio function calls.
    Expects JSON input with function_name and arguments.
    """
    try:
        # Read input from LMStudio
        if len(sys.argv) > 1:
            # Command line argument input
            input_data = sys.argv[1]
        else:
            # Stdin input
            input_data = sys.stdin.read().strip()
        
        # Parse the JSON input
        try:
            call_data = json.loads(input_data)
        except json.JSONDecodeError:
            print(json.dumps({
                "success": False,
                "error": "Invalid JSON input"
            }))
            return
        
        # Extract function name and arguments
        function_name = call_data.get("function_name")
        arguments = call_data.get("arguments", {})
        
        if not function_name:
            print(json.dumps({
                "success": False,
                "error": "Missing function_name in input"
            }))
            return
        
        # Call the filesystem handler
        result = handle_function_call(function_name, arguments)
        print(result)
        
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": f"Bridge error: {str(e)}"
        }))

if __name__ == "__main__":
    main()
