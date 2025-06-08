# LMStudio Structured Output Configuration

## 🎯 Purpose
This JSON schema forces LMStudio to generate consistent function calls in the proper OpenAI format.

## 📋 Setup Instructions

### Step 1: Enable Structured Output in LMStudio
1. Open LMStudio
2. Load your Qwen2.5-Coder model
3. Start Local Server (port 1234)
4. Find "Structured Output" toggle in settings
5. **Enable** the toggle ✅

### Step 2: Paste This JSON Schema
Copy the entire JSON below and paste it into the schema field:

```json
{
  "type": "object",
  "properties": {
    "content": {
      "type": "string",
      "description": "The assistant's response content"
    },
    "tool_calls": {
      "type": "array",
      "description": "Function calls to execute",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string",
            "description": "Unique identifier for the tool call"
          },
          "type": {
            "type": "string",
            "enum": ["function"],
            "description": "Type of tool call"
          },
          "function": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "enum": [
                  "read_file",
                  "write_file", 
                  "list_directory",
                  "create_directory",
                  "search_files",
                  "get_file_info"
                ],
                "description": "Name of the function to call"
              },
              "arguments": {
                "type": "string",
                "description": "JSON string of function arguments"
              }
            },
            "required": ["name", "arguments"],
            "additionalProperties": false
          }
        },
        "required": ["id", "type", "function"],
        "additionalProperties": false
      }
    }
  },
  "required": ["content"],
  "additionalProperties": false
}
```

### Step 3: Test Function Calling
```bash
cd /Users/admin/Documents/Qwen_Coder_Local/src
python qwen_filesystem_integration_v2.py
```

Try: "List files in current directory"

## 🎯 Expected Behavior
With this schema, Qwen should generate responses like:
```json
{
  "content": "I'll list the files in the current directory for you.",
  "tool_calls": [
    {
      "id": "call_123",
      "type": "function",
      "function": {
        "name": "list_directory",
        "arguments": "{\"path\": \".\"}"
      }
    }
  ]
}
```

## 🔧 Alternative: Simpler Schema
If the above doesn't work, try this minimal version:
```json
{
  "type": "object",
  "properties": {
    "response": {
      "type": "string",
      "description": "Assistant response with XML tool calls: <tool_call>{\"name\": \"function\", \"arguments\": {}}</tool_call>"
    }
  },
  "required": ["response"]
}
```

This forces the XML format that matches your Jinja template.

## 🎉 Success Indicators
- ✅ No schema validation errors
- ✅ Function calls appear in responses
- ✅ Filesystem operations execute automatically
- ✅ Natural conversation with file access

Your framework is ready - this configuration step will complete the integration! 🚀
