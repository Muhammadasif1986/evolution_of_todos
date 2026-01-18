---
id: "006"
title: "Update Model to Qwen Qwen3-Coder"
stage: "misc"
date: "2026-01-16"
surface: "agent"
model: "Sonnet 4.5"
feature: "003-ai-todo-chatbot"
branch: "003-ai-todo-chatbot"
user: "asif_abdulqadir"
command: "Update AI model to qwen/qwen3-coder:free as requested by user"
labels: ["ai", "model", "tool-calling", "fix", "openrouter"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "/mnt/d/quater-4 hackathons/Hackathon-2/phase-2/backend/src/ai/ai_agent.py"
tests: []
---

# PHR: Update Model to Qwen Qwen3-Coder

## Summary
Updated AI model to qwen/qwen3-coder:free as requested by the user.

## User Prompt
```
qwen/qwen3-coder:free try this model
```

## Response Summary
Changed the AI model from "microsoft/phi-3-mini-128k-instruct:free" to "qwen/qwen3-coder:free" in the ai_agent.py file as specifically requested by the user.

## Technical Details

### Model Change
- Changed model from "microsoft/phi-3-mini-128k-instruct:free" to "qwen/qwen3-coder:free" in `/mnt/d/quater-4 hackathons/Hackathon-2/phase-2/backend/src/ai/ai_agent.py`
- Updated both locations where the model is referenced
- Qwen Qwen3-Coder is a model that's available as a free tier model on OpenRouter
- This model has function calling capabilities and should work with the existing tool configuration

## Outcome
The AI agent will now use qwen/qwen3-coder:free as the model for processing requests. This model was specifically requested by the user.

## Evaluation
- [x] Updated model in initial API call
- [x] Updated model in follow-up API call
- [x] Used model as specifically requested by user
- [x] Maintained all other functionality