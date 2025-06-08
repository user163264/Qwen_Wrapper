#!/usr/bin/env python3
"""
Qwen Filesystem API Integration Script
Connects Qwen2.5-Coder model running in LMStudio to local filesystem operations.
"""

import json
import sys
import os
from pathlib import Path
from openai import OpenAI

# Add the src directory to Python path so we can import our filesystem handler
sys.path.append(str(Path(__file__).parent))
from filesystem_handler import FilesystemHandler

class QwenFilesystemIntegration:
    def __init__(self, base_url="http://localhost:1234/v1", model="qwen2.5-coder-1.5b-instruct"):
        """Initialize the integration with LMStudio API."""
        self.client = OpenAI(
            base_url=base_url,
            api_key="not-needed-for-local"  # LMStudio doesn't require API key
        )
        self.model = model
        self.filesystem_handler = FilesystemHandler()
        
        # Define the function schemas for Qwen
        self.function_schemas = [
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read the complete contents of a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Path to the file to read"}
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function", 
                "function": {
                    "name": "write_file",
                    "description": "Write content to a file (creates new or overwrites existing)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Path to the file to write"},
                            "content": {"type": "string", "description": "Content to write to the file"}
                        },
                        "required": ["path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "append_to_file", 
                    "description": "Append content to an existing file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Path to the file to append to"},
                            "content": {"type": "string", "description": "Content to append to the file"}
                        },
                        "required": ["path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_directory",
                    "description": "List all files and directories in a given path",
                    "parameters": {
                        "type": "object", 
                        "properties": {
                            "path": {"type": "string", "description": "Path to the directory to list"}
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_directory",
                    "description": "Create a new directory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Path to the directory to create"}
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function", 
                "function": {
                    "name": "delete_file",
                    "description": "Delete a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Path to the file to delete"}
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_directory", 
                    "description": "Delete a directory (must be empty)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Path to the directory to delete"}
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "move_file",
                    "description": "Move or rename a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "source": {"type": "string", "description": "Source path of the file"},
                            "destination": {"type": "string", "description": "Destination path for the file"}
                        },
                        "required": ["source", "destination"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "copy_file",
                    "description": "Copy a file to a new location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "source": {"type": "string", "description": "Source path of the file"},
                            "destination": {"type": "string", "description": "Destination path for the copy"}
                        },
                        "required": ["source", "destination"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_files",
                    "description": "Search for files and directories matching a pattern",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Directory to search in"},
                            "pattern": {"type": "string", "description": "Search pattern/filename to match"}
                        },
                        "required": ["path", "pattern"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_file_info",
                    "description": "Get detailed information about a file or directory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Path to get information about"}
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_allowed_directories",
                    "description": "Get list of directories the AI can access",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            }
        ]
    
    def execute_function(self, function_name, arguments):
        """Execute a filesystem function and return the result."""
        try:
            # Get the method from filesystem handler
            method = getattr(self.filesystem_handler, function_name)
            
            # Execute the function with arguments
            if arguments:
                result = method(**arguments)
            else:
                result = method()
            
            return result
            
        except AttributeError:
            return {
                "success": False,
                "error": f"Unknown function: {function_name}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Function execution error: {str(e)}"
            }
    
    def chat_with_filesystem_access(self, user_message, conversation_history=None):
        """
        Send a message to Qwen with filesystem access capabilities.
        Returns the complete conversation including function calls.
        """
        if conversation_history is None:
            conversation_history = []
        
        # Add user message to conversation
        messages = conversation_history + [{"role": "user", "content": user_message}]
        
        # Make the API call with function schemas
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.function_schemas,
                tool_choice="auto"  # Let the model decide when to use tools
            )
            
            # Get the assistant's response
            assistant_message = response.choices[0].message
            messages.append({
                "role": "assistant", 
                "content": assistant_message.content,
                "tool_calls": assistant_message.tool_calls
            })
            
            # Check if the model wants to call functions
            if assistant_message.tool_calls:
                print(f"\n🔧 Qwen is calling {len(assistant_message.tool_calls)} function(s)...")
                
                # Execute each function call
                for tool_call in assistant_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    print(f"  📁 Executing: {function_name}({function_args})")
                    
                    # Execute the function
                    result = self.execute_function(function_name, function_args)
                    
                    # Add function result to conversation
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result)
                    })
                
                # Get the model's response after function execution
                second_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
                
                final_message = second_response.choices[0].message
                messages.append({
                    "role": "assistant",
                    "content": final_message.content
                })
                
                return {
                    "response": final_message.content,
                    "conversation": messages,
                    "functions_called": len(assistant_message.tool_calls)
                }
            
            else:
                # No function calls, just return the response
                return {
                    "response": assistant_message.content,
                    "conversation": messages,
                    "functions_called": 0
                }
                
        except Exception as e:
            return {
                "response": f"Error communicating with Qwen: {str(e)}",
                "conversation": messages,
                "functions_called": 0,
                "error": True
            }
    
    def interactive_chat(self):
        """Start an interactive chat session with Qwen."""
        print("🤖 Qwen Filesystem Assistant Ready!")
        print("📁 Available directories:", self.filesystem_handler.get_allowed_directories()["allowed_directories"])
        print("💬 Type 'quit' to exit, 'help' for commands\n")
        
        conversation_history = []
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                if user_input.lower() == 'clear':
                    conversation_history = []
                    print("🧹 Conversation history cleared!")
                    continue
                
                if not user_input:
                    continue
                
                # Get response from Qwen
                result = self.chat_with_filesystem_access(user_input, conversation_history)
                
                # Update conversation history
                conversation_history = result["conversation"]
                
                # Display response
                if result.get("functions_called", 0) > 0:
                    print(f"\n🤖 Qwen (after calling {result['functions_called']} function(s)): {result['response']}")
                else:
                    print(f"\n🤖 Qwen: {result['response']}")
                
                if result.get("error"):
                    print("⚠️  There was an error in the conversation.")
                
                print()  # Add spacing
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def show_help(self):
        """Show available commands and capabilities."""
        print("\n📖 Qwen Filesystem Assistant Help")
        print("=" * 40)
        print("Commands:")
        print("  help  - Show this help message")
        print("  clear - Clear conversation history")
        print("  quit  - Exit the assistant")
        print("\nFilesystem Capabilities:")
        print("  📄 Read, write, and append to files")
        print("  📁 List, create, and delete directories")
        print("  🔍 Search for files and get file info")
        print("  📋 Copy and move files")
        print("  🔒 Secure access to allowed directories only")
        print("\nExample Requests:")
        print("  'Create a Python script that prints hello world'")
        print("  'List all files in the current directory'")
        print("  'Read the contents of README.md'")
        print("  'Create a new directory called test_folder'")
        print("  'Search for all .py files in the project'")
        print()

def main():
    """Main entry point for the integration script."""
    print("🚀 Starting Qwen Filesystem Integration...")
    
    # Check if filesystem handler exists
    handler_path = Path(__file__).parent / "filesystem_handler.py"
    if not handler_path.exists():
        print("❌ Error: filesystem_handler.py not found!")
        print(f"   Expected location: {handler_path}")
        return
    
    try:
        # Initialize the integration
        integration = QwenFilesystemIntegration()
        
        # Test connection to LMStudio
        print("🔌 Testing connection to LMStudio...")
        test_response = integration.client.chat.completions.create(
            model=integration.model,
            messages=[{"role": "user", "content": "Hello! Can you confirm you're working?"}],
            max_tokens=50
        )
        print("✅ LMStudio connection successful!")
        print(f"🧠 Model: {integration.model}")
        
        # Start interactive session
        integration.interactive_chat()
        
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure LMStudio server is running (localhost:1234)")
        print("2. Verify Qwen model is loaded in LMStudio")
        print("3. Check that filesystem_handler.py exists in the same directory")

if __name__ == "__main__":
    main()
