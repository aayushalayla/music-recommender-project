# AI Music Recommender System

## Project Summary

This project upgrades my Module 3 project, `ai110-module3show-musicrecommendersimulation-starter`, into a fuller applied AI system. The original project was a music recommender simulation that scored songs based on user preferences such as mood, genre, and activity. It demonstrated the basic logic of recommendation systems, but it did not yet include retrieval, validation, testing, or an inspectable AI workflow.

The upgraded system is a Streamlit-based AI music recommender. A user enters a listening request, such as “dreamy sad songs for studying” or “chaotic workout music,” and the system validates the input, retrieves relevant song and context data, generates recommendations, calculates a confidence score, and shows an agent trace explaining how the result was produced.

I think recommendation systems shape cultural discovery. A useful recommender should not only return songs; it should also make its reasoning visible, handle weak inputs safely, and be testable.

## Core AI Features

This project includes four applied AI system features:

1. **Multi-source retrieval / RAG-style retrieval**
   - The system retrieves from `data/songs.csv`.
   - It also retrieves listening-context guidance from `data/listening_contexts.csv`.
   - This lets the system use both song metadata and situational context before generating recommendations.

2. **Agentic workflow**
   - The recommender follows a visible multi-step process:
     1. Validate user input.
     2. Retrieve relevant songs and context guidance.
     3. Compare baseline retrieval with enhanced retrieval.
     4. Generate recommendations.
     5. Validate that recommendations came from retrieved data.
     6. Calculate confidence.
   - The Streamlit app displays these steps in an **Agent Trace** section.

3. **Specialized recommendation behavior**
   - The user can choose different recommendation styles:
     - Plain
     - Music Critic
     - Study Companion
     - DJ
   - These styles change how the system explains its recommendations.

4. **Reliability and evaluation**
   - The system includes automated tests.
   - It includes confidence scoring.
   - It includes guardrails for vague or empty input.
   - It includes an evaluation script, `scripts/evaluate_system.py`, that runs predefined prompts and prints pass/fail results.

## Architecture Overview

The system follows this structure:

```text
User Input
   ↓
Guardrails / Input Validation
   ↓
Multi-Source Retriever
   ├── data/songs.csv
   └── data/listening_contexts.csv
   ↓
Agentic Recommendation Workflow
   ↓
Specialized Recommendation Generator
   ↓
Evaluator
   ├── confidence scoring
   ├── recommendation validation
   └── baseline vs enhanced retrieval comparison
   ↓
Streamlit Output
   ├── recommendations
   ├── confidence score
   ├── agent trace
   ├── RAG enhancement measurement
   └── specialization comparison