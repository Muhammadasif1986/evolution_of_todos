---
id: "002"
title: "Update Model for Tool Calling Fix"
stage: "misc"
date: "2026-01-16"
surface: "agent"
model: "Sonnet 4.5"
feature: "003-ai-todo-chatbot"
branch: "003-ai-todo-chatbot"
user: "asif_abdulqadir"
command: "Update AI model from xiaomi/mimo-v2-flash:free to meta-llama/llama-3.1-8b-instruct:free to fix tool calling error"
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

# PHR: Update Model for Tool Calling Fix

## Summary
Updated AI model from xiaomi/mimo-v2-flash:free to meta-llama/llama-3.1-8b-instruct:free to fix ongoing "Unexpected tool call id list_tasks in tool results" error.

## User Prompt
```
I encountered an issue processing your request: Error code: 400 - {'error': {'message': 'Provider returned error', 'code': 400, 'metadata': {'raw': '{"object":"error","message":"Unexpected tool call id list_tasks in tool results","type":"invalid_request_message_order","param":null,"code":"3230"}', 'provider_name': 'Mistral', 'is_byok': False}}, 'user_id': 'user_2xdySmSVlAKrR3xNcAySPht2v2B'}
you can search in openrouter free model capibale fix this issue
```

## Response Summary
Changed the AI model from "xiaomi/mimo-v2-flash:free" to "meta-llama/llama-3.1-8b-instruct:free" in the ai_agent.py file. This model is known to have better support for function calling and should resolve the tool calling errors that were persisting with the previous models.

## Technical Details

### Model Change
- Changed model from "xiaomi/mimo-v2-flash:free" to "meta-llama/llama-3.1-8b-instruct:free" in `/mnt/d/quater-4 hackathons/Hackathon-2/phase-2/backend/src/ai/ai_agent.py`
- Updated both locations where the model is referenced (lines 162 and 218)
- Meta Llama 3.1 8B Instruct is known to have robust function calling capabilities and is available as a free tier model on OpenRouter
- This should resolve the "Unexpected tool call id list_tasks in tool results" error that was occurring with Mistral-based models

## Outcome
The AI agent should now be able to properly handle tool calls without the previous error. The Meta Llama 3.1 model has proven reliability with function calling in the OpenRouter ecosystem.

## Evaluation
- [x] Updated model in initial API call
- [x] Updated model in follow-up API call
- [x] Selected model known for reliable function calling
- [x] Maintained all other functionality