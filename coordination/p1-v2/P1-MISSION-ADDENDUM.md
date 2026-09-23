# P1 mission, vision and review standard (founder, 2026-09-23 — verbatim)

> This is the founder's authoritative statement of what P1 must achieve. It overrides every design document. The build spec
> (`P1-V2-BUILD-SPEC.md`) is one way to meet it; where they disagree, this document wins.

## 1. Purpose of this addendum

This addendum establishes the authoritative product objective against which Media Intelligence P1 must be independently reviewed.
The review must evaluate whether the existing implementation achieves the intended product outcome, not merely whether it satisfies its current architecture, implementation checklist, or previously written engineering specifications.
The existing product design is evidence of what was intended and implemented. It is not, by itself, the definition of success.
The reviewer must independently establish whether the system is capable of delivering the customer experience described below.

## 2. The vision

Build an AI-native creative production company, delivered as software.
Enable businesses to turn an idea, product, or commercial objective into exceptional media without needing to understand filmmaking, design, generative models, prompt engineering, or production infrastructure.
The customer should experience Media Intelligence as a capable creative agency and production studio.
They supply the problem, product information, creative requirements, and necessary approvals.
The system takes responsibility for creative development, production planning, execution, quality verification, and delivery.
The long-term ambition is to make professional creative intelligence and production capability accessible, scalable, reliable, and economically viable.

## 3. The P1 mission

Deliver the first working, customer-facing AI creative production system capable of producing commercially acceptable images and short videos from real customer briefs.
P1 must bring together:

* Creative intelligence and the existing Canon.
* Structured understanding of customer requirements.
* Professional creative direction and storytelling.
* Evidence-based production planning and model selection.
* Reliable image, video, audio, editing, and compositing capabilities.
* Independent verification of the actual generated media.
* Targeted repair and customer acceptance.
* Operational reuse of previous production learning.
* A complete, accessible customer-facing product.

P1 is not complete merely because these capabilities exist independently.
They must work together to deliver acceptable finished media through the actual customer journey.

## 4. The core customer promise

A D2C brand, FMCG company, marketing team, or commercial-media buyer should be able to approach Media Intelligence with a product and an objective.
For example:
"Create a memorable 30-second advertisement for our travel backpack that communicates its extraordinary capacity."
The system should:

1. Understand the customer's objective, audience, product, and mandatory requirements.
2. Retrieve relevant brand information, Canon knowledge, and verified production experience.
3. Develop a compelling creative idea appropriate to the assignment.
4. Translate that idea into an executable visual and sound treatment.
5. Select production methods capable of achieving the intended result.
6. Generate and assemble actual media.
7. Independently inspect the finished work for creative, product, continuity, audio, and technical quality.
8. Repair defects without unnecessarily rebuilding unaffected work.
9. Present the result for customer approval.
10. Deliver the accepted media and record what the production taught the system.

The customer should not need a developer to operate these steps manually.
The fundamental outcome is:
The customer receives a finished piece of media that satisfies their requirements, communicates the intended message, and is good enough for its intended commercial use.

## 5. The creative-director standard

Review P1 through the perspective of an established professional creative production team.
Consider the complementary working principles associated with Ridley Scott, Spike Jonze, and Prasoon Pandey:

* Cinematic composition, visual storytelling, atmosphere, and coherent world-building.
* Original concepts, human emotion, performance, humour, and memorable visual ideas.
* Consumer understanding, cultural relevance, commercial communication, and meaningful product integration.

These perspectives are not prescriptions to imitate any particular filmmaker.
They represent the level of creative reasoning and production responsibility the system is intended to embody.
The reviewer must examine whether the creative intelligence genuinely understands the assignment and develops an effective creative solution.
A valid storyboard, detailed prompt, or attractive individual shot is not sufficient.
The completed work must communicate its intended idea and deliver a coherent audience experience.
Creative quality must be evaluated independently from engineering correctness.

## 6. What P1 must prove

Evaluate the product against the following seven outcomes.

**A. Creative intelligence** — Can the system understand a real commercial assignment, retrieve relevant knowledge, develop an original concept, and translate it into a coherent, compelling creative execution? Does the creative direction serve the customer's objective rather than merely produce visually impressive material?

**B. Production intelligence** — Can the system convert the creative treatment into an executable plan and select appropriate production techniques based on demonstrated capabilities? Does it recognize when a generative model is unlikely to execute a required physical action, product interaction, continuity requirement, or complex visual sequence? Does it choose a workable production approach rather than repeatedly asking an unsuitable model to perform the same action?

**C. Actual media quality** — Does the finished media satisfy the original assignment? For images, inspect composition, product fidelity, brand identity, copy, visual hierarchy, and commercial communication. For videos, inspect the complete film: story, performances, physical actions, shot continuity, cinematography, pacing, editing, sound, product identity, and overall audience experience. Evaluate the work as the intended customer or audience would experience it, including at representative viewing size. Do not infer quality from the underlying prompts, forms, or technical specifications.

**D. Production reliability** — Can the complete workflow execute without a developer manually coordinating every stage? Can it handle provider failures, interrupted jobs, budget limits, rejected assets, and targeted revisions? Does the system preserve approved creative decisions and reusable assets? Does the actual production pathway invoke the relevant existing protections?

**E. Operational learning** — Does each new production inherit applicable verified solutions from previous jobs? The existing historical failure atlas and production-learning records must be examined. A failure mechanism appearing in a register is not proof that its protection operates. Distinguish failures prevented before spending, detected and repaired before presentation, knowingly accepted with an authorized exception, and defects that reached the customer. P1 should not require repeated rediscovery of previously solved engineering problems.

**F. Customer experience** — Can a real customer submit a brief, provide assets, answer essential questions, review the creative direction, approve production, receive a preview, request changes, and download accepted media? Does the system make ordinary creative and technical decisions autonomously? Does it avoid exposing unnecessary internal complexity or relying on developer intervention?

**G. Production economics** — Can the system deliver commercially acceptable media within a practical customer waiting time and economically sustainable production cost? The target for a supported 30-second commercial is a customer-presentable first cut within approximately 10–15 minutes of an approved, production-ready brief, with a target AI production cost of approximately USD 5–15. These are intended performance targets, not established service levels. Evaluate actual measured latency, total expenditure, failed attempts, repairs, and Cost per Accepted Outcome. Do not treat speed or low generation cost as success when the customer rejects the output.

## 7–10. Method, treatment of the 23 September outcomes, exclusions, required outcome

Start from the intended customer outcome and work backward. For each finding: intended behaviour → actual implementation and evidence → what the system did → did it meet the requirement → earliest consequential failure → cause vs symptom → which control should have caught it → isolated or architectural → smallest reliable intervention. Do not prescribe changes only because they differ from a preferred architecture; do not keep a failing architecture because effort was invested in it.

Do not measure success by: completed engineering tasks; Canon sources or packs; forms or agents implemented; passing unit tests alone; a complete storyboard; successful API calls; a technically valid file; an unqualified model review; a within-budget production the customer rejects; a demonstration requiring repeated developer intervention. Do not turn the work into another indefinite Canon, research, governance or architecture workstream. Do not add complexity without naming the concrete product failure it resolves.

**Final standard:** a real business gives the system a creative assignment and receives a finished advertisement or image it is willing to accept and use commercially, without managing the creative and production process itself. A technically functional system that repeatedly produces rejected media has not achieved the P1 mission. An exceptional result produced through extensive manual developer intervention has not demonstrated the intended product either.
