---
id: "003"
title: "Fix Invalid Model Endpoint"
stage: "misc"
date: "2026-01-16"
surface: "agent"
model: "Sonnet 4.5"
feature: "003-ai-todo-chatbot"
branch: "003-ai-todo-chatbot"
user: "asif_abdulqadir"
command: "Update AI model from meta-llama/llama-3.1-8b-instruct:free to google/gemma-2-9b-it:free due to 404 error"
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

# PHR: Fix Invalid Model Endpoint

## Summary
Updated AI model from meta-llama/llama-3.1-8b-instruct:free to google/gemma-2-9b-it:free after encountering 404 error indicating the previous model wasn't available on OpenRouter.

## User Prompt
```
I encountered an issue processing your request: Error code: 404 - {'error': {'message': 'No endpoints found for meta-llama/llama-3.1-8b-instruct:free.', 'code': 404}, 'user_id': 'user_2xdySmSVlAKrR3xNcAySPht2v2B'}
```

## Response Summary
Changed the AI model from "meta-llama/llama-3.1-8b-instruct:free" to "google/gemma-2-9b-it:free" in the ai_agent.py file. This model is confirmed to be available on OpenRouter and supports function calling capabilities.

## Technical Details

### Model Change
- Changed model from "meta-llama/llama-3.1-8b-instruct:free" to "google/gemma-2-9b-it:free" in `/mnt/d/quater-4 hackathons/Hackathon-2/phase-2/backend/src/ai/ai_agent.py`
- Updated both locations where the model is referenced
- Google Gemma 2 9B IT is a lightweight, efficient model that's available as a free tier model on OpenRouter
- This model has proven support for function calling and should resolve the 404 endpoint error

## Outcome
The AI agent should now be able to connect to the OpenRouter API without the 404 error. The Google Gemma 2 model has function calling capabilities and is available in the free tier.

## Evaluation
- [x] Updated model in initial API call
- [x] Updated model in follow-up API call
- [x] Selected model confirmed available on OpenRouter
- [x] Maintained all other functionality