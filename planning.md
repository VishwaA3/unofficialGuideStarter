# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

The domain that I chose is making student advice and tips of surviving freshman year at NJIT. This knowledge is valuable and hard to find through official channels because it covers practical topics like registration, parking, food, disability accommodations, orientation, and whether NJIT is worth the cost. This is the kind of advice upperclassmen share informally but new students struggle to find it all in one place. Official NJIT resources rarely capture this raw perspective of navigating the first week feels of being a freshman, leaving incoming students to rely on Reddit threads and word-of-mouth to get useful answers.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | r/NJTech | Comprehensive guide to CS at NJIT — courses, professors, tips | https://www.reddit.com/r/NJTech/comments/cq8oi8/my_guide_to_computer_science_at_njit/ |
| 2 | r/NJTech | Tips for incoming freshmen, especially commuters | https://www.reddit.com/r/NJTech/comments/4wx1xv/some_tips_to_all_incoming_freshmen_more_commuter/ |
| 3 | r/NJTech | FAQ thread for incoming freshmen | https://www.reddit.com/r/NJTech/comments/1t7be07/faq_for_incoming_freshmen/ |
| 4 | r/NJTech | Student discussion on whether NJIT is worth $20k/year in debt | https://www.reddit.com/r/NJTech/comments/1jc2ayt/is_njit_worth_20k_a_year_in_debt_in_your_opinion/ |
| 5 | r/NJTech | Student experiences with disability accommodations and OARS | https://www.reddit.com/r/NJTech/comments/1q3u5gm/how_supportive_is_njit_for_disability_students/ |
| 6 | r/NJTech | Commuter parking tips and cost-saving strategies near NJIT | https://www.reddit.com/r/NJTech/comments/1n03vat/what_are_some_costefficient_or_free_ways_i_can/ |
| 7 | r/NJTech | Student-recommended food spots around NJIT campus | https://www.reddit.com/r/NJTech/comments/bwv0tk/solid_food_around_njit/ |
| 8 | r/NJTech | General Q&A thread for students new to NJIT | https://www.reddit.com/r/NJTech/comments/3el6hm/new_to_njit_got_questions_ask_them_here/ |
| 9 | r/NJTech | First-year guide covering registration, GPA, tutoring, and key websites | https://www.reddit.com/r/NJTech/comments/1lbme48/for_upcoming_first_years/ |
| 10 | r/NJTech | Student experiences and honest takes on NSO 2.0 | https://www.reddit.com/r/NJTech/comments/1mu07w0/nso_20_why_is_it_almost_a_full_day/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 500 characters

**Overlap:** 100 characters

**Reasoning:** My documents include short student tips, Q&A, and longer guides from students on r/NJTech. A 500 character chunk is big enough to include the entire piece of advice or tip, without merging unrelated topics together. Chunks smaller than 500 characters hold the risk of cutting the advice mid-sentence, and this would serve no use. Chucks largers than 500 characters would combine multiple topics into one piece, whether they are related or not. This would make it hard to match specific queries and questions. A 100 character overlap ensures that the advice split across a chunk boundary is still retrievable. An example is if a parking tip starts at the endo f one chunk, then the next tip will also contain its beginning from the previous chunk.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** sentence-transformers (all-MiniLM-L6-v2)

**Top-k:** 4

**Production tradeoff reflection:** 
If I was deploying this project for real users and cost wasn't a constraint, the following are tradeoffs I'd weigh in when it comes to choosing a different embedding model. 

- **Context Length:** When it comes to context length, all-MiniLM-L6-v2 has a 256-token limit per chunk. This means that longer documents, such as advice guides that can span till multiple paragraphs, would cut off useful content. A model with a greater token limit would allow greater chunk sizes, preventing them from getting cut off when the token limit is reached. 
- **Multilingual Support:**  For multilingual support, I'd use a multilingual model considering the fact that NJIT has a large international student population. A multilingual model would allow non-English speakers to query in their native languages as well. 
- **Accuracy on Domain-Specific Text:** A model that is trained on student or forum-styled text, for example: Reddit data, would retrieve more relevant chunks of data for more casual and quick-questions styled queries. 
- **Latency:** For a personal project like this one, the smaller/local model is efficient, providing quicker responses with no cost. However, a larger model that is trained on way more data and contains a lot more layers holds a better ability to understand specific and complex queries. However, with a greater model comes latency. When it comes to a real app with real users, I'd need to carefully compare and analyze whether the accuracy that comes with a larger model is worth it for the latency and cost.  

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What are some free or cheap parking options near NJIT for commuters? | Park west of Lock St, on Boyden St, or on Central Ave near Dunkin; NJ Transit student pass is 25% cheaper than standard monthly; NJIT semester parking pass costs $325 |
| 2 | What GPA do you need to stay in good academic standing at NJIT? | 2.0+ in both Overall GPA and Term GPA; Dean's List requires 3.0+ with no failed classes; Greek Life requires 2.6+ minimum |
| 3 | How do disability accommodations work at NJIT through OARS? | Submit paperwork to OARS (not directly to professors); fill out a form 3-4 days before each exam; OARS contacts professors on your behalf; get documentation in early before semester starts |
| 4 | What do students say about whether NJIT is worth the cost? | Most recommend going to community college first for Gen Eds to save money; NJIT dorms cost $5000+ per semester; University Centre nearby costs ~$800/month; graduates report strong salaries |
| 5 | What food spots near NJIT have student discounts? | Burger Walla, Meatball Obsession, Masala Cafe, Fresh Coast (20% off 2-5pm), Turkish Pita Place, Halal Guys (10% with NJIT ID) |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.**Key facts split across chunks:** Some of my source documents contain long survival guides for freshmen, providing helpful tips and suggestions structures in long sentences. A 500-character chunk has the risk of cutting a tip in half, resulting in one half of the tip being in one chunk and the other half being in the other chunk. However, neither chunk alone fully answers that question, and at the time of retrieval, only one of them might be returned.

2.**User queries including informal language:** Some user queries by students may include slang terms, informal words, or abbreviations that the embedding model may struggle to match with the formal phrasing from the source documents. This poses a risk of the retrieval missing relevant information from the chunks. 

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

![Pipeline Diagram](mermaidDiagram.png)
---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
My plan is to use Claude. 
For input, I'll be providing my 10 source documents, (.txt files in /sources folder). I will also be providing my Chunking Strategy of 500 characters and 100 characters overlap. 
For output, I expect Claude to create a script that loads all the .txt files, cleans any remaining unnecessary information in the files, and splits them into chunks with the specified size and overlap, along with attaching the source filename as metadata to each chunk. 
Then, I'll verify that my output matches the specification by printing out some random chunks and checking that they are readable, relevant, and under 500 characters. 

**Milestone 4 — Embedding and retrieval:**
My plan is to use Claude. 
For input, I'll be providing my Retrieval Approach of using all-MiniLM-L6-v2, ChromaDB, top-k=4. Along with that, I'll also provide my pipeline diagram. 
For output, I expect Claude to implement an embedding script that loads chunks from Milestone 3, embeds them from all-MiniLM-L6-v2, stores them in ChromaDB with source metadata, and returns the top 4 chunks for a query. 
Then, I'll verify this by running 3 of my evaluation questions on the chunks to check that they are relevant and have distance scores close to 0, meaning that they are similar to the query and so a good match. 

**Milestone 5 — Generation and interface:**
My plan is to use Claude. 
For input, I'll be providing my grounding requirement of drawing answers only from retrieval text and including the source metadata. 
For output, I will ask Claude to implement a function to generate using Groq's llama-3.3-70b-versatile that takes retrieved chunks as context and then returns an answer with the source cited. I will also ask Claude to build a Gradio interface with a input box for queries, answer output, and a source citation output. 
Then, I'll verify this by testing with a out of the box question that my documents do not cover, and checking whether my system correctly declines to answer rather than hallucinating an answer. 