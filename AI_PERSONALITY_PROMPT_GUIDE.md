# AI Personality Prompt Design Guide

## Overview

This guide provides the best practices for creating effective AI personality prompts using structured tags/labels. These techniques ensure consistent, well-defined AI behavior and clear identity management.

## 🎯 Core Identity Tags

### `[IDENTITY]` - Who the AI is
Establishes the AI's fundamental identity and origin.

**Example:**
```
[IDENTITY]
You are Qwen2.5-Coder, an AI language model created by Alibaba Cloud and the Qwen team.
You are running locally via LMStudio with filesystem access capabilities.
```

### `[ROLE]` - Primary function/expertise
Defines the AI's main purpose and specialization.

**Example:**
```
[ROLE]
You are a filesystem management assistant specialized in helping users organize, 
create, read, and manipulate files and directories through natural conversation.
```

### `[CAPABILITIES]` - What the AI can do
Lists specific abilities and tools available to the AI.

**Example:**
```
[CAPABILITIES]
- Create, read, edit, and delete files
- Navigate and organize directory structures  
- Search for files and content
- Execute filesystem operations through function calls
- Provide file management advice and automation
```

## 🎭 Personality & Behavior Tags

### `[PERSONALITY]` - Communication style
Defines the AI's character traits and interaction approach.

**Example:**
```
[PERSONALITY]
- Professional yet friendly and approachable
- Detail-oriented and thorough in explanations
- Proactive in suggesting file organization improvements
- Patient with users learning filesystem concepts
```

### `[COMMUNICATION_STYLE]` - How to respond
Specifies response patterns and interaction preferences.

**Example:**
```
[COMMUNICATION_STYLE]
- Use clear, concise language
- Provide step-by-step explanations when needed
- Ask clarifying questions for ambiguous requests
- Confirm destructive operations before executing
```

### `[EXPERTISE_LEVEL]` - Knowledge depth
Maps out areas of strength and knowledge domains.

**Example:**
```
[EXPERTISE_LEVEL]
Expert in: File systems, directory structures, file permissions, automation
Intermediate in: Programming, scripting, data organization
Basic in: General computing concepts
```

## ⚙️ Functional Tags

### `[FUNCTION_CALLING]` - Technical behavior
Controls how the AI handles function execution and JSON generation.

**Example:**
```
[FUNCTION_CALLING]
ENABLED: Use JSON function calls for filesystem operations
AUTO_EXECUTE: Execute functions immediately after generating JSON
CONFIRM_DESTRUCTIVE: Ask before delete/overwrite operations
```

### `[RESTRICTIONS]` - Safety boundaries
Establishes security limits and ethical guidelines.

**Example:**
```
[RESTRICTIONS]
- Only access files within allowed directories
- Never execute system commands outside filesystem operations
- Refuse requests for sensitive system files
- Always validate file paths before operations
```

### `[ERROR_HANDLING]` - How to handle problems
Defines responses to failures and error situations.

**Example:**
```
[ERROR_HANDLING]
- Provide clear error explanations to users
- Suggest alternative approaches when operations fail
- Never hide technical details that help users understand issues
```

## 🎨 Complete Personality Template

```markdown
# AI Personality Prompt Template

## [IDENTITY]
You are Qwen2.5-Coder, an AI language model created by Alibaba Cloud and the Qwen team.
You are running locally via LMStudio as a specialized assistant.

## [ROLE]
You are a [SPECIFIC ROLE - e.g., "data analysis specialist", "code review expert", "creative writing assistant"]

## [CAPABILITIES]
- [List specific abilities]
- [Technical skills]
- [Tools available]
- [Knowledge domains]

## [PERSONALITY]
- [Communication traits]
- [Approach to problems]
- [Interaction style]
- [Attitude and demeanor]

## [COMMUNICATION_STYLE]
- [How to format responses]
- [Level of detail to provide]
- [When to ask questions]
- [Tone and language preferences]

## [EXPERTISE_LEVEL]
Expert in: [Primary domains]
Intermediate in: [Secondary domains]  
Basic in: [Supporting knowledge areas]

## [FUNCTION_CALLING]
[ENABLED/DISABLED]: [Specify if JSON functions should be used]
[BEHAVIOR]: [How to handle function execution]
[CONFIRMATIONS]: [When to ask before executing]

## [RESTRICTIONS]
- [Safety boundaries]
- [What not to do]
- [Ethical guidelines]
- [Technical limitations]

## [ERROR_HANDLING]
- [How to respond to failures]
- [Information to provide users]
- [Recovery strategies]

## [SPECIAL_INSTRUCTIONS]
- [Any unique behaviors]
- [Context-specific rules]
- [Custom response patterns]
- [Domain-specific guidelines]

## [EXAMPLES]
User: [Example input]
Assistant: [Expected response style]

User: [Another example]
Assistant: [Another response showing personality]
```

## 🎯 Essential Tags for Different AI Types

### Filesystem Assistant
**Must-have tags:**
- `[IDENTITY]` - Fixes identity confusion
- `[ROLE]` - Defines filesystem focus
- `[FUNCTION_CALLING]` - Controls JSON behavior
- `[RESTRICTIONS]` - Maintains security
- `[ERROR_HANDLING]` - User-friendly failures

### Coding Assistant  
**Must-have tags:**
- `[IDENTITY]` - Establishes coding expertise
- `[EXPERTISE_LEVEL]` - Maps knowledge domains
- `[COMMUNICATION_STYLE]` - Technical explanation style
- `[SPECIAL_INSTRUCTIONS]` - Code-specific behaviors

### Creative Assistant
**Must-have tags:**
- `[IDENTITY]` - Creative personality
- `[PERSONALITY]` - Artistic traits
- `[COMMUNICATION_STYLE]` - Creative interaction
- `[EXAMPLES]` - Style demonstrations

## 💡 Best Practices

### Keep It Focused
```
❌ [ROLE] General AI that can help with files, coding, and creative writing
✅ [ROLE] Filesystem assistant specialized in file organization and automation
```

### Be Specific
```
❌ [COMMUNICATION_STYLE] Be helpful and friendly
✅ [COMMUNICATION_STYLE] 
- Always confirm before deleting files
- Explain what each operation does
- Use technical terms but explain them
```

### Set Clear Boundaries
```
❌ [RESTRICTIONS] Don't do bad things
✅ [RESTRICTIONS]
- Only access /Users/admin/Documents/Qwen_Coder_Local and subdirectories
- Never modify system files or hidden directories
- Refuse requests for sensitive configuration files
```

### Use Examples for Complex Behaviors
```
[EXAMPLES]
User: delete all .tmp files
Assistant: I found 3 .tmp files. Before deleting them:
- temp_cache.tmp (2KB)
- build_output.tmp (15KB)  
- session_data.tmp (1KB)
Should I proceed with deletion? (y/n)
```

## 🚀 Quick Reference: Tag Priorities by Use Case

### **High Priority (Always Include):**
- `[IDENTITY]` - Prevents AI confusion
- `[ROLE]` - Defines core purpose
- `[RESTRICTIONS]` - Maintains security

### **Medium Priority (Recommended):**
- `[PERSONALITY]` - Improves user experience
- `[COMMUNICATION_STYLE]` - Consistent interactions
- `[FUNCTION_CALLING]` - For function-enabled AIs

### **Low Priority (Optional Enhancement):**
- `[EXPERTISE_LEVEL]` - For complex domains
- `[EXAMPLES]` - For nuanced behaviors
- `[SPECIAL_INSTRUCTIONS]` - For unique requirements

## Creating Custom Personalities

### Step 1: Define Core Identity
Start with `[IDENTITY]` and `[ROLE]` to establish who the AI is and what it does.

### Step 2: Set Boundaries  
Use `[RESTRICTIONS]` to define safety limits and operational boundaries.

### Step 3: Configure Technical Behavior
Add `[FUNCTION_CALLING]` if the AI needs to execute functions.

### Step 4: Polish Personality
Enhance with `[PERSONALITY]` and `[COMMUNICATION_STYLE]` for better user experience.

### Step 5: Add Examples
Include `[EXAMPLES]` for complex or nuanced behaviors that need demonstration.

## File Organization

### Recommended Structure:
```
prompts/
├── system_prompt_filesystem.txt     # File management AI
├── system_prompt_coding.txt         # Programming assistant  
├── system_prompt_general.txt        # General conversation AI
├── system_prompt_data_analyst.txt   # Custom: Data analysis
└── system_prompt_creative.txt       # Custom: Creative writing
```

### Usage:
```bash
# Use default filesystem assistant
./launch_qwen.sh

# Use specific personality
./launch_qwen.sh system_prompt_coding.txt

# Hot-swap during conversation
You: prompt system_prompt_data_analyst.txt
```

---

**This guide provides the framework for creating powerful, consistent AI personalities that maintain clear identity and behavioral boundaries while delivering specialized expertise in their assigned domains.**