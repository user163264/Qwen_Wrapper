#!/usr/bin/env python3
"""
Qwen Filesystem API Integration Script - Version 5
EXTENDS V4 WITH CODE ANALYSIS CAPABILITIES
"""

import json
import sys
import os
import re
from pathlib import Path
from openai import OpenAI

# Add the src directory to Python path so we can import our handlers
sys.path.append(str(Path(__file__).parent))
from filesystem_handler import FilesystemHandler
from code_analyzer import analyze_code, explain_code, get_code_metrics, extract_functions, find_dependencies, debug_code, optimize_code

class QwenFilesystemIntegrationV5:
    def __init__(self, base_url="http://localhost:1234/v1", system_prompt_file=None):
        """Initialize the integration with LMStudio API and code analysis."""
        self.client = OpenAI(
            base_url=base_url,
            api_key="lm-studio"  # Some versions need a dummy key
        )
        self.model = None  # Will be auto-detected
        self.filesystem_handler = FilesystemHandler()
        
        # Load system prompt from file or use default
        self.system_prompt = self.load_system_prompt(system_prompt_file)
    
    def load_system_prompt(self, prompt_file=None):
        """Load system prompt from file or use default."""
        if prompt_file:
            try:
                # Handle both absolute and relative paths
                if not os.path.isabs(prompt_file):
                    # Look in prompts directory
                    prompts_dir = Path(__file__).parent.parent / "prompts"
                    prompt_path = prompts_dir / prompt_file
                else:
                    prompt_path = Path(prompt_file)
                
                if prompt_path.exists():
                    with open(prompt_path, 'r', encoding='utf-8') as f:
                        prompt = f.read().strip()
                    print(f"✅ Loaded system prompt from: {prompt_path}")
                    return prompt
                else:
                    print(f"⚠️  System prompt file not found: {prompt_path}")
                    print("📝 Using default enhanced filesystem prompt")
            except Exception as e:
                print(f"❌ Error loading system prompt: {e}")
                print("📝 Using default enhanced filesystem prompt")
        
        # Enhanced default system prompt with code analysis
        return """You are Qwen2.5-Coder, an AI language model created by Alibaba Cloud and the Qwen team. You are running locally via LMStudio and have advanced filesystem access and code analysis capabilities through function calling.

CRITICAL: You must ONLY use the exact function names listed below. Never create, guess, or use any other function names.

When users request file operations or code analysis, respond with JSON in this exact format:

{
  "response": "Your natural language response to the user",
  "tool_calls": [
    {
      "type": "function",
      "function": {
        "name": "EXACT_FUNCTION_NAME_FROM_LIST_BELOW",
        "arguments": {"key": "value"}
      }
    }
  ]
}

AVAILABLE FUNCTIONS (USE EXACTLY THESE NAMES):

FILESYSTEM OPERATIONS:
- read_file
- write_file
- list_directory
- create_directory
- search_files
- get_file_info

CODE ANALYSIS OPERATIONS:
- analyze_code
- explain_code
- get_code_metrics
- extract_functions
- find_dependencies
- debug_code
- optimize_code

FUNCTION USAGE EXAMPLES:

For "analyze the code in sample.cpp":
{
  "response": "I'll analyze the code in sample.cpp for you.",
  "tool_calls": [
    {
      "type": "function",
      "function": {
        "name": "read_file",
        "arguments": {"path": "sample.cpp"}
      }
    },
    {
      "type": "function",
      "function": {
        "name": "analyze_code",
        "arguments": {"path": "sample.cpp"}
      }
    }
  ]
}

NEVER use function names like:
- disassemble_code
- parse_code
- process_code
- review_code
- examine_code

ONLY use the exact function names from the list above.

Always respond with valid JSON when operations are requested. Be helpful, accurate, and maintain your identity as Qwen2.5-Coder running locally with enhanced code analysis capabilities."""
    
    def auto_detect_model(self):
        """Auto-detect the loaded model in LMStudio"""
        try:
            # Try common model names
            model_attempts = [
                "qwen2.5-coder-1.5b-instruct",
                "Qwen2.5-Coder-1.5B-Instruct",
                "qwen2.5-coder",
                None  # Let OpenAI client auto-detect
            ]
            
            for model_name in model_attempts:
                try:
                    response = self.client.chat.completions.create(
                        model=model_name,
                        messages=[{"role": "user", "content": "Hi"}],
                        max_tokens=10
                    )
                    self.model = model_name
                    print(f"✅ Detected model: {model_name or 'auto-detected'}")
                    return True
                except:
                    continue
                    
            return False
        except Exception as e:
            print(f"❌ Model detection failed: {e}")
            return False
    
    def execute_function(self, function_name, arguments):
        """Execute a filesystem or code analysis function and return the result."""
        try:
            # List of all valid function names
            valid_functions = [
                'read_file', 'write_file', 'list_directory', 'create_directory', 'search_files', 'get_file_info',
                'analyze_code', 'explain_code', 'get_code_metrics', 'extract_functions', 'find_dependencies', 'debug_code', 'optimize_code'
            ]
            
            # Check if function name is valid
            if function_name not in valid_functions:
                return {
                    "success": False,
                    "error": f"Unknown function: {function_name}. Valid functions are: {', '.join(valid_functions)}"
                }
            
            # Handle code analysis functions
            if function_name in ['analyze_code', 'explain_code', 'get_code_metrics', 'extract_functions', 'find_dependencies', 'debug_code', 'optimize_code']:
                return self.execute_code_analysis_function(function_name, arguments)
            
            # Handle filesystem functions (existing V4 code)
            method = getattr(self.filesystem_handler, function_name)
            
            # Map generic 'path' parameter to function-specific parameter names
            if arguments and 'path' in arguments:
                path_value = arguments['path']
                if function_name in ['read_file', 'write_file']:
                    arguments['file_path'] = path_value
                    del arguments['path']
                elif function_name == 'list_directory':
                    arguments['directory_path'] = path_value
                    del arguments['path']
                elif function_name == 'create_directory':
                    arguments['directory_path'] = path_value
                    del arguments['path']
                elif function_name == 'search_files':
                    arguments['search_path'] = path_value
                    del arguments['path']
                    # Fix common search patterns
                    if 'pattern' in arguments:
                        pattern = arguments['pattern']
                        # Convert regex-style patterns to glob patterns
                        if pattern.startswith('\\') and pattern.endswith('$'):
                            arguments['pattern'] = pattern.replace('\\.py$', '*.py').replace('\\', '').replace('$', '')
                # get_file_info uses 'path' so no change needed
            
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
    
    def execute_code_analysis_function(self, function_name, arguments):
        """Execute code analysis functions."""
        try:
            # All code analysis functions require a 'path' parameter
            if 'path' not in arguments:
                return {
                    "success": False,
                    "error": "Code analysis functions require a 'path' parameter"
                }
            
            file_path = arguments['path']
            
            # Map function names to their implementations
            if function_name == 'analyze_code':
                result = analyze_code(file_path)
                return {"success": True, "analysis": result}
            
            elif function_name == 'explain_code':
                start_line = arguments.get('start_line')
                end_line = arguments.get('end_line')
                explanation = explain_code(file_path, start_line, end_line)
                return {"success": True, "explanation": explanation}
            
            elif function_name == 'get_code_metrics':
                metrics = get_code_metrics(file_path)
                return {"success": True, "metrics": metrics}
            
            elif function_name == 'extract_functions':
                functions = extract_functions(file_path)
                return {"success": True, "functions": functions}
            
            elif function_name == 'find_dependencies':
                dependencies = find_dependencies(file_path)
                return {"success": True, "dependencies": dependencies}
            
            elif function_name == 'debug_code':
                debug_result = debug_code(file_path)
                return {"success": True, "debug_analysis": debug_result}
            
            elif function_name == 'optimize_code':
                optimization_result = optimize_code(file_path)
                return {"success": True, "optimization_analysis": optimization_result}
            
            else:
                return {
                    "success": False,
                    "error": f"Unknown code analysis function: {function_name}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Code analysis error: {str(e)}"
            }
    
    def parse_response(self, response_text):
        """Parse response text to extract JSON function calls."""
        try:
            # Try to parse as direct JSON
            data = json.loads(response_text)
            return data
        except json.JSONDecodeError:
            # Try to find JSON in the response
            json_pattern = r'\{[^{}]*"tool_calls"[^{}]*\[[^\]]*\][^{}]*\}'
            matches = re.findall(json_pattern, response_text, re.DOTALL)
            
            for match in matches:
                try:
                    data = json.loads(match)
                    return data
                except:
                    continue
            
            # Return as plain text response
            return {
                "response": response_text,
                "tool_calls": []
            }
    
    def chat_with_filesystem_access(self, user_message, conversation_history=None):
        """Send a message to Qwen with filesystem access and code analysis capabilities."""
        if conversation_history is None:
            conversation_history = []
        
        # Build messages with system prompt
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1500,  # Increased for code analysis responses
                temperature=0.1  # Lower temperature for more consistent JSON
            )
            
            response_text = response.choices[0].message.content
            
            # Parse the response
            parsed_response = self.parse_response(response_text)
            
            # Add to conversation history
            conversation_history.append({"role": "user", "content": user_message})
            conversation_history.append({"role": "assistant", "content": response_text})
            
            functions_executed = 0
            function_results = []
            
            # Execute any function calls
            if "tool_calls" in parsed_response and parsed_response["tool_calls"]:
                print(f"\n🔧 Processing {len(parsed_response['tool_calls'])} function call(s)...")
                
                for tool_call in parsed_response["tool_calls"]:
                    if "function" in tool_call:
                        function_name = tool_call["function"]["name"]
                        function_args = tool_call["function"]["arguments"]
                        
                        print(f"  📁 Calling: {function_name}({function_args})")
                        
                        # Execute function
                        result = self.execute_function(function_name, function_args)
                        function_results.append({
                            "function": function_name,
                            "args": function_args,
                            "result": result
                        })
                        functions_executed += 1
                        
                        # Show brief result summary
                        if result.get("success", True):
                            if "items" in result:
                                print(f"  ✅ Found {len(result['items'])} items")
                            elif "matches" in result:
                                print(f"  ✅ Found {len(result['matches'])} matches")
                            elif "content" in result:
                                print(f"  ✅ Read {len(result['content'])} characters")
                            elif "analysis" in result:
                                print(f"  ✅ Code analysis complete")
                            elif "explanation" in result:
                                print(f"  ✅ Code explanation generated")
                            elif "metrics" in result:
                                print(f"  ✅ Code metrics calculated")
                            elif "functions" in result:
                                print(f"  ✅ Found {len(result['functions'])} functions")
                            elif "dependencies" in result:
                                print(f"  ✅ Found {len(result['dependencies'])} dependencies")
                            elif "message" in result:
                                print(f"  ✅ {result['message']}")
                            else:
                                print(f"  ✅ Success")
                        else:
                            print(f"  ❌ Error: {result.get('error', 'Unknown error')}")
            
            return {
                "response": parsed_response.get("response", response_text),
                "conversation": conversation_history,
                "functions_called": functions_executed,
                "function_results": function_results,
                "raw_response": response_text
            }
                
        except Exception as e:
            print(f"❌ API Error: {e}")
            return {
                "response": f"Connection error: {str(e)}",
                "conversation": conversation_history,
                "functions_called": 0,
                "error": True
            }
    
    def interactive_chat(self):
        """Start an interactive chat session with Qwen."""
        print("🤖 Qwen Filesystem Assistant V5 Ready!")
        print("🆕 WITH ADVANCED CODE ANALYSIS CAPABILITIES!")
        
        print("\n📁 Available directories:", self.filesystem_handler.get_allowed_directories()["allowed_directories"])
        print("💬 Type 'quit' to exit, 'help' for commands")
        print("🎯 Try: 'what does sample.cpp do?' or 'analyze main.py'\n")
        
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
                
                if user_input.lower().startswith('prompt '):
                    # Change system prompt on the fly
                    prompt_file = user_input[7:].strip()
                    self.system_prompt = self.load_system_prompt(prompt_file)
                    conversation_history = []  # Clear history when changing prompts
                    print("🔄 System prompt updated and conversation history cleared!")
                    continue
                
                if not user_input:
                    continue
                
                # Get response from Qwen
                result = self.chat_with_filesystem_access(user_input, conversation_history)
                
                # Update conversation history
                conversation_history = result["conversation"]
                
                # Display response with context
                if result.get("functions_called", 0) > 0:
                    print(f"\n🤖 Qwen (executed {result['functions_called']} function(s)): {result['response']}")
                    
                    # Show detailed function results
                    for func_result in result.get("function_results", []):
                        func_name = func_result['function']
                        func_data = func_result['result']
                        
                        if func_data.get("success", True):
                            print(f"   📁 {func_name}: ✅ Success")
                            
                            # Display specific results based on function type
                            if func_name == 'list_directory' and 'items' in func_data:
                                items = func_data['items']
                                print(f"     📂 Directory contents ({len(items)} items):")
                                for item in items:
                                    icon = "📁" if item['type'] == 'directory' else "📄"
                                    print(f"       {icon} {item['name']}")
                            
                            elif func_name == 'read_file' and 'content' in func_data:
                                content = func_data['content']
                                print(f"     📄 File content ({func_data.get('size', 0)} bytes):")
                                if len(content) > 200:
                                    print(f"       {content[:200]}...")
                                else:
                                    print(f"       {content}")
                            
                            elif func_name == 'search_files' and 'matches' in func_data:
                                matches = func_data['matches']
                                if matches:
                                    print(f"     🔍 Search results ({len(matches)} matches):")
                                    for match in matches:
                                        icon = "📁" if match['type'] == 'directory' else "📄"
                                        print(f"       {icon} {match['name']} ({match['path']})")
                                else:
                                    print(f"     🔍 No files found matching pattern '{func_data.get('pattern', '')}'")
                            
                            elif func_name == 'write_file' and 'message' in func_data:
                                print(f"     📝 {func_data['message']} ({func_data.get('size', 0)} bytes)")
                            
                            elif func_name == 'create_directory' and 'message' in func_data:
                                print(f"     📂 {func_data['message']}")
                            
                            elif func_name == 'get_file_info':
                                info = func_data
                                icon = "📁" if info.get('type') == 'directory' else "📄"
                                print(f"     {icon} File info: {info.get('name', '')}")
                                print(f"       Size: {info.get('size', 0)} bytes")
                                print(f"       Modified: {info.get('modified', 'Unknown')}")
                                print(f"       Type: {info.get('type', 'Unknown')}")
                            
                            # Code analysis function results
                            elif func_name == 'analyze_code' and 'analysis' in func_data:
                                analysis = func_data['analysis']
                                print(f"     🔍 Code Analysis Results:")
                                if 'file_info' in analysis:
                                    info = analysis['file_info']
                                    print(f"       Language: {info.get('language', 'Unknown')}")
                                    print(f"       Lines: {info.get('line_count', 0)}")
                                if 'summary' in analysis:
                                    print(f"       Summary: {analysis['summary']}")
                                if 'metrics' in analysis:
                                    metrics = analysis['metrics']
                                    print(f"       Functions: {metrics.get('function_count', 0)}")
                                    print(f"       Classes: {metrics.get('class_count', 0)}")
                                    print(f"       Complexity: {metrics.get('complexity_estimate', 0)}")
                            
                            elif func_name == 'explain_code' and 'explanation' in func_data:
                                print(f"     📖 Code Explanation:")
                                print(f"       {func_data['explanation']}")
                            
                            elif func_name == 'get_code_metrics' and 'metrics' in func_data:
                                metrics = func_data['metrics']
                                print(f"     📊 Code Metrics:")
                                print(f"       Total lines: {metrics.get('total_lines', 0)}")
                                print(f"       Code lines: {metrics.get('code_lines', 0)}")
                                print(f"       Functions: {metrics.get('function_count', 0)}")
                                print(f"       Classes: {metrics.get('class_count', 0)}")
                                print(f"       Complexity: {metrics.get('complexity_estimate', 0)}")
                                print(f"       Comment ratio: {metrics.get('comment_ratio', 0)}%")
                            
                            elif func_name == 'extract_functions' and 'functions' in func_data:
                                functions = func_data['functions']
                                print(f"     🎯 Functions found ({len(functions)}):")
                                for func in functions:
                                    print(f"       • {func.get('name', 'Unknown')} (line {func.get('line', '?')})")
                            
                            elif func_name == 'find_dependencies' and 'dependencies' in func_data:
                                deps = func_data['dependencies']
                                print(f"     🔗 Dependencies found ({len(deps)}):")
                                for dep in deps:
                                    print(f"       • {dep}")
                        else:
                            print(f"   📁 {func_name}: ❌ {func_data.get('error')}")
                else:
                    print(f"\n🤖 Qwen: {result['response']}")
                
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def show_help(self):
        """Show available commands and capabilities."""
        print("\n📖 Qwen Filesystem Assistant V5 Help")
        print("=" * 50)
        print("🆕 Enhanced with advanced code analysis capabilities!")
        print("\nCommands:")
        print("  help                    - Show this help message")
        print("  clear                   - Clear conversation history")
        print("  prompt <filename>       - Load new system prompt from file")
        print("  quit                    - Exit the assistant")
        print("\nFilesystem Operations:")
        print("  'Create hello.txt with Hello World content'")
        print("  'List files in current directory'")
        print("  'Read the hello.txt file'")
        print("  'Search for all .py files'")
        print("\nCode Analysis Operations (NEW):")
        print("  'What does sample.cpp do?'              - Comprehensive analysis")
        print("  'Analyze main.py'                       - Detailed code breakdown")
        print("  'Explain the main function in app.py'   - Code explanation")
        print("  'Show me metrics for project.py'        - Code statistics")
        print("  'List all functions in utils.py'        - Function extraction")
        print("  'What libraries does main.py use?'      - Dependency analysis")
        print("\nAvailable System Prompts:")
        prompts_dir = Path(__file__).parent.parent / "prompts"
        if prompts_dir.exists():
            for prompt_file in prompts_dir.glob("*.txt"):
                print(f"  📝 {prompt_file.name}")
        print("\nExample Prompt Changes:")
        print("  prompt system_prompt_coding.txt     - Switch to coding assistant")
        print("  prompt system_prompt_general.txt    - Switch to general assistant")
        print("  prompt system_prompt_filesystem.txt - Switch to basic filesystem mode")
        print()

def main():
    """Main entry point for the integration script v5."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Qwen Filesystem Assistant V5 with Code Analysis")
    parser.add_argument("--prompt", "-p", help="System prompt file to load")
    args = parser.parse_args()
    
    print("🚀 Starting Qwen Filesystem Integration V5...")
    print("🆕 WITH ADVANCED CODE ANALYSIS CAPABILITIES!")
    
    try:
        # Initialize the integration
        integration = QwenFilesystemIntegrationV5(system_prompt_file=args.prompt)
        
        # Auto-detect model
        if not integration.auto_detect_model():
            print("❌ Could not connect to LMStudio or detect model")
            print("\n🔧 Troubleshooting:")
            print("1. Ensure LMStudio server is running (localhost:1234)")
            print("2. Load a Qwen model in LMStudio")
            print("3. Enable API server in LMStudio")
            return
        
        # Start interactive session
        integration.interactive_chat()
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        print("\n🔧 Check:")
        print("1. LMStudio running on localhost:1234")
        print("2. Model loaded and API server started")
        print("3. filesystem_handler.py and code_analyzer.py exist")

if __name__ == "__main__":
    main()
