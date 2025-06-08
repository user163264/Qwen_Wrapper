# Qwen Filesystem Access Framework

🚀 **A complete AI filesystem integration that gives Qwen2.5-Coder natural language control over local files and advanced code analysis capabilities.**

## ✨ What This Does

Transforms your local Qwen 2.5-Coder model into a powerful filesystem assistant that can:

- 📁 **Read, write, and manage files** through natural conversation
- 🔍 **Analyze code** in multiple languages (Python, C++, JavaScript, Java)
- 🐛 **Debug and optimize** code automatically
- 🎭 **Switch AI personalities** on-demand for different tasks
- 🛡️ **Secure operation** with directory restrictions

## 🎯 Quick Start

```bash
# Make launcher executable
chmod +x launch_qwen.sh

# Start the enhanced system (filesystem + code analysis)
./launch_qwen.sh

# Or start with specific AI personality
./launch_qwen.sh system_prompt_coding.txt
```

**Test it:**
```
You: what files are in this directory?
You: what does sample.cpp do?
You: create a new file called hello.txt with "Hello World"
You: debug this Python code
```

## 🌟 Key Features

### **🤖 Multiple AI Personalities**
- **Enhanced Assistant**: Full filesystem + code analysis
- **Filesystem Assistant**: File management specialist  
- **Coding Assistant**: Programming help and review
- **General Assistant**: Questions and explanations

### **📁 Filesystem Operations (6 functions)**
- Read/write files
- Create/list directories
- Search files by pattern
- Append to files

### **🔍 Code Analysis (7 functions)**
- Comprehensive code analysis
- Bug detection and security analysis
- Performance optimization suggestions
- Dependency mapping
- Function extraction
- Code explanation in plain English
- Quality metrics and complexity analysis

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   LM Studio     │────│  Function Calls  │────│  Python Handler │
│  (Qwen Model)   │    │   (JSON Schema)   │    │ (Secure Wrapper)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────│ AI Personalities│──────────────┘
                        │  (Text Prompts) │
                        └─────────────────┘
```

## 🛡️ Security Model

- **Directory Restrictions**: Only allowed directories accessible
- **Path Validation**: All paths sanitized and validated
- **Error Handling**: Graceful failure modes
- **Permission Checks**: Respects filesystem permissions

## 📊 System Status

✅ **V5 Enhanced System**: Production ready with full testing
✅ **18 Total Functions**: All filesystem and code analysis operations
✅ **Hot-swappable Prompts**: Change AI behavior during conversation
✅ **LM Studio Integration**: Multiple integration methods
✅ **Security Framework**: Directory restrictions and validation
✅ **Documentation**: Complete guides and examples

## 🔧 Integration Options

### **Option 1: Enhanced CLI (Recommended)**
```bash
./launch_qwen.sh  # Full capabilities
```

### **Option 2: LM Studio Function Server**
```bash
python src/lmstudio_function_server.py  # Background server
# Use LM Studio GUI with function calling
```

### **Option 3: Direct Python Integration**
```bash
python src/qwen_filesystem_integration_v5.py
```

## 📚 Documentation

- **`SETUP_GUIDE.md`**: Detailed setup instructions
- **`SYSTEM_PROMPTS_README.md`**: AI personality configuration
- **`AI_PERSONALITY_PROMPT_GUIDE.md`**: Creating custom personalities
- **`LMSTUDIO_FUNCTION_CALLING_GUIDE.md`**: LM Studio integration

## 🎯 Use Cases

- **Development**: Code analysis, debugging, file management
- **Learning**: Code explanation and optimization guidance
- **Automation**: Natural language file operations
- **Research**: Project analysis and documentation

## 🚀 Example Session

```
You: analyze the main.py file
🔧 Processing 2 function call(s)...
  📁 read_file: ✅ Read 1247 characters
  🔍 analyze_code: ✅ Analysis complete
🤖 This Python file contains a FastAPI web application with 3 endpoints...

You: what can be optimized?
🔧 Processing 1 function call(s)...
  ⚡ optimize_code: ✅ Found 4 optimization opportunities
🤖 Performance improvements: Use async/await for database calls...

You: create a backup of this file
🔧 Processing 1 function call(s)...
  📁 write_file: ✅ File created successfully
🤖 Created backup as main_backup.py
```

---

**Built for Qwen2.5-Coder 1.5B Instruct running on LM Studio**

*Transform your local AI into a powerful development assistant!* 🎉
