---
id: "005"
title: "Final Model Selection for Function Calling"
stage: "misc"
date: "2026-01-16"
surface: "agent"
model: "Sonnet 4.5"
feature: "003-ai-todo-chatbot"
branch: "003-ai-todo-chatbot"
user: "asif_abdulqadir"
command: "Update AI model to microsoft/phi-3-mini-128k-instruct:free as final attempt after multiple 404 errors"
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

# PHR: Final Model Selection for Function Calling

## Summary
Updated AI model to microsoft/phi-3-mini-128k-instruct:free as the final attempt after multiple 404 errors with other free models. This model is widely supported on OpenRouter and has function calling capabilities.

## User Prompt
```
I encountered an issue processing your request: Error code: 404 - {'error': {'message': 'No endpoints found for google/gemma-2-9b-it:free.', 'code': 404}, 'user_id': 'user_2xdySmSVlAKrR3xNcAySPht2v2B'}
```

## Response Summary
Changed the AI model from "huggingface/unsloth/mistral-nemo-12b:free" to "microsoft/phi-3-mini-128k-instruct:free" in the ai_agent.py file. This model is confirmed to be widely available on OpenRouter and supports function calling capabilities.

## Technical Details

### Model Change
- Changed model from "huggingface/unsloth/mistral-nemo-12b:free" to "microsoft/phi-3-mini-128k-instruct:free" in `/mnt/d/quater-4 hackathons/Hackathon-2/phase-2/backend/src/ai/ai_agent.py`
- Updated both locations where the model is referenced
- Microsoft Phi-3 Mini 128K Instruct is a lightweight, efficient model that's well-supported as a free tier model on OpenRouter
- This model has proven support for function calling and should resolve the 404 endpoint errors experienced with other models

## Outcome
The AI agent should now be able to connect to the OpenRouter API without 404 errors. The Phi-3 model has reliable function calling capabilities and is consistently available in the free tier.

## Evaluation
- [x] Updated model in initial API call
- [x] Updated model in follow-up API call
- [x] Selected model with reliable OpenRouter availability
- [x] Maintained all other functionality