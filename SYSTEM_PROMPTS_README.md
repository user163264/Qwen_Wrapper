# 📝 System Prompts Guide

## 🎯 Overview
Version 4 of the Qwen Filesystem Assistant supports loading system prompts from text files, making it easy to customize the AI's behavior without editing code.

## 📁 Available System Prompts

### `system_prompt_filesystem.txt` (Default)
- **Purpose**: Full filesystem operations with function calling
- **Use Case**: File management, development tasks, project organization
- **Features**: Creates, reads, lists, searches files through natural language

### `system_prompt_coding.txt`
- **Purpose**: Focused coding assistant
- **Use Case**: Programming help, code review, debugging
- **Features**: Expert programming advice, clean code examples

### `system_prompt_general.txt`
- **Purpose**: General AI assistant
- **Use Case**: Questions, explanations, general conversation
- **Features**: Helpful conversation without filesystem operations

## 🚀 How to Use

### Method 1: Command Line Arguments
```bash
# Use default filesystem prompt
python src/qwen_filesystem_integration_v4.py

# Use coding assistant
python src/qwen_filesystem_integration_v4.py --prompt system_prompt_coding.txt

# Use general assistant
python src/qwen_filesystem_integration_v4.py --prompt system_prompt_general.txt
```

### Method 2: Launcher Script
```bash
# Make executable first
chmod +x launch_qwen.sh

# Use default
./launch_qwen.sh

# Use specific prompt
./launch_qwen.sh system_prompt_coding.txt
./launch_qwen.sh system_prompt_general.txt
```

### Method 3: Change Prompts During Chat
```
You: prompt system_prompt_coding.txt
🔄 System prompt updated and conversation history cleared!

You: help me write a Python function
🤖 Qwen: I'd be happy to help you write a Python function! What do you need it to do?
```

## ✏️ Creating Custom Prompts

1. **Create a new `.txt` file** in the `prompts/` directory
2. **Write your system prompt** (see examples in existing files)
3. **Load it** using any of the methods above

### Example Custom Prompt (`prompts/my_custom_prompt.txt`):
```
You are Qwen2.5-Coder, a specialized assistant for [YOUR USE CASE].

[YOUR INSTRUCTIONS HERE]

Always maintain your identity as Qwen2.5-Coder by Alibaba Cloud.
```

## 🔧 File Paths

The system looks for prompts in these locations:
1. **Relative to prompts directory**: `system_prompt_coding.txt` → `prompts/system_prompt_coding.txt`
2. **Absolute paths**: `/full/path/to/prompt.txt`
3. **Current directory**: `./my_prompt.txt`

## 💡 Tips

- **Filesystem Operations**: Only use `system_prompt_filesystem.txt` for file operations
- **Conversation History**: Gets cleared when switching prompts
- **Identity**: Always include Qwen2.5-Coder identity to prevent confusion
- **JSON Format**: Only filesystem prompt includes JSON function calling instructions

## 🎯 Use Cases

### Development Work
```bash
./launch_qwen.sh system_prompt_filesystem.txt
# Then: "Create a Python project structure with main.py and requirements.txt"
```

### Code Help
```bash
./launch_qwen.sh system_prompt_coding.txt  
# Then: "Review this Python function for bugs"
```

### General Questions
```bash
./launch_qwen.sh system_prompt_general.txt
# Then: "Explain quantum computing in simple terms"
```

## 🚀 Advanced Usage

### Multiple Assistants
Run different prompts in separate terminals:
```bash
# Terminal 1: File manager
./launch_qwen.sh system_prompt_filesystem.txt

# Terminal 2: Coding help
./launch_qwen.sh system_prompt_coding.txt
```

### Quick Switching
Use the `prompt` command to switch personalities:
```
You: prompt system_prompt_coding.txt
You: help me debug this code
You: prompt system_prompt_filesystem.txt  
You: create a backup of important files
```

This gives you maximum flexibility to use Qwen exactly how you need it! 🎉
