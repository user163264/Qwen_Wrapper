# LMStudio Function Calling Configuration Guide

## The Problem
Your Qwen integration is complete and working, but LMStudio isn't triggering function calls. Based on your Jinja template, function calling IS supported, but needs proper configuration.

## Quick Diagnosis
Run this first to confirm the issue:
```bash
cd /Users/admin/Documents/Qwen_Coder_Local
python test_function_calling_v2.py
```

## LMStudio Configuration Steps

### 1. Check LMStudio Version
- **Required**: LMStudio 0.3.6 or newer
- **Recommended**: Latest version from lmstudio.ai
- Function calling support was added in recent versions

### 2. Model Requirements
- ✅ **Your Model**: Qwen2.5-Coder-1.5B-Instruct supports function calling
- ✅ **Location**: Your model path is correct
- ✅ **Format**: GGUF format is compatible

### 3. LMStudio Settings to Check

#### In LMStudio Interface:
1. **Load Model**: Ensure Qwen2.5-Coder is loaded
2. **Server Settings**: 
   - Port: 1234 (default)
   - API Endpoint: Enable
   - OpenAI Compatible: Enable
3. **Function Calling Settings** (if available):
   - Enable "Function Calling" or "Tools"
   - Set "Tool Choice" to "Auto"
   - Enable "Structured Output" (if option exists)

#### Advanced Settings to Try:
- **Template**: Your Jinja template shows function calling support ✅
- **Context Length**: Increase if too low (8192+ recommended)
- **Temperature**: Try 0.1-0.7 for more deterministic function calling
- **Top-p**: Try 0.8-0.95

### 4. Prompt Template Verification
Your Jinja template includes this function calling section:
```jinja
{%- if tools %}
    {{- "\n\n# Tools\n\nYou may call one or more functions to assist with the user query.\n\nYou are provided with function signatures within <tools></tools> XML tags:\n<tools>" }}
    {%- for tool in tools %}
        {{- "\n" }}
        {{- tool | tojson }}
    {%- endfor %}
    {{- "\n</tools>\n\nFor each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:\n<tool_call>\n{{\"name\": <function-name>, \"arguments\": <args-json-object>}}\n</tool_call><|im_end|>\n" }}
{%- endif %}
```

This confirms function calling IS supported. The issue is likely configuration.

### 5. Testing Different Approaches

Try the improved integration script:
```bash
cd /Users/admin/Documents/Qwen_Coder_Local/src
python qwen_filesystem_integration_v2.py
```

This version:
- Auto-detects the model
- Tests multiple function calling formats
- Provides better error reporting
- Has fallback mode for debugging

## Troubleshooting Checklist

### ❌ If Function Calling Still Not Working:

1. **Check LMStudio Logs**:
   - Look for errors about "tools" or "functions"
   - Check if tools parameter is being ignored

2. **Try Different Model Settings**:
   - Reload the model
   - Try different quantization (if available)
   - Clear model cache

3. **API Format Issues**:
   - Some LMStudio versions expect specific formats
   - Try simplified tools format (without "type": "function")

4. **Network/Connection**:
   - Restart LMStudio server
   - Try different port (1235, 8080)
   - Check firewall settings

### ✅ If Basic Chat Works But No Functions:

Your project has a **fallback mode** that works immediately:
```bash
python qwen_fallback.py
```

This gives you filesystem access through text commands while you debug function calling.

## Alternative Solutions

### Option 1: Manual Function Calling
If LMStudio doesn't support automatic function calling, you can:
1. Train Qwen to output function calls in the expected format
2. Parse the text response for function call patterns
3. Execute functions based on parsed text

### Option 2: Different Model
Try a model explicitly known to work with LMStudio function calling:
- Different Qwen variant
- Code-specific models with confirmed tool support

### Option 3: Different Platform
Your integration could work with:
- Ollama + Qwen (often better function calling support)
- Local OpenAI-compatible servers (vLLM, text-generation-inference)

## Expected Behavior When Working

When function calling works, you should see:
```
You: List files in current directory
🔧 Qwen is calling 1 function(s)...
  📁 Executing: list_directory({'path': '.'})
🤖 Qwen (after calling 1 function): I found 15 files in the current directory including...
```

## Next Steps

1. **Run the comprehensive test**: `python test_function_calling_v2.py`
2. **Check LMStudio settings** for function calling options
3. **Try the v2 integration**: `python qwen_filesystem_integration_v2.py`
4. **Use fallback mode** if needed: `python qwen_fallback.py`

Your core integration is solid - this is just a configuration issue!
