#!/usr/bin/env python3
"""
DVNC.ai – Chainlit Integration
Leonardo da Vinci-inspired AI System with Interactive Web Interface
"""

import chainlit as cl
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime

# ---------- Domain Model ----------

@dataclass
class FineTunedSLM:
    domain: str
    knowledge: Dict[str, str]
    temperature: float = 0.6
    system_prompt: str = field(init=False)

    def __post_init__(self):
        self.system_prompt = (
            f"You are a specialized SLM for {self.domain}. "
            f"Use concise, actionable language. Cite a Da Vinci study when relevant. "
            f"Prefer design heuristics and constraints over vague generalities."
        )

    def _choose(self, items: List[str]) -> str:
        if not items:
            return random.choice(list(self.knowledge.keys()))
        if self.temperature >= 0.7 and len(items) > 1:
            return random.choice(items)
        return items[0]

    def generate_insight(self, prompt_keywords: List[str], user_prompt: str) -> str:
        if not prompt_keywords:
            concept = self._choose([])
            study = self.knowledge[concept]
            return (
                f"Consider **{concept}**, informed by da Vinci's work on *{study}*. "
                f"Translate this into constraints and a measurable performance target."
            )

        chosen_kw = self._choose(prompt_keywords)
        concept = None
        for k in self.knowledge.keys():
            if chosen_kw.lower() == k.lower() or chosen_kw.lower() in k.lower():
                concept = k
                break
        if not concept:
            concept = self._choose(list(self.knowledge.keys()))

        study = self.knowledge[concept]
        return (
            f"Leverage **{concept}** (cf. da Vinci's *{study}*). "
            f"Define 2–3 constraints, an objective, and a quick benchtop test."
        )

# ---------- System Orchestration ----------

class DVNCSystem:
    def __init__(self, include_domain: str = "Anatomy", seed: int = 42):
        random.seed(seed)
        
        self.physics_knowledge = {
            "Fluid Dynamics": "water screws and canal studies",
            "Aerodynamics": "ornithopter sketches and airflow notes",
            "Lever Mechanics": "gear trains, pulleys, cranes",
            "Structural Integrity": "bridges and fortification stress studies",
        }
        self.biomech_knowledge = {
            "Joint Articulation": "elbow/shoulder motion notebooks",
            "Muscular Force": "layered muscle drawings",
            "Biological Levers": "limb lever ratios and gait notes",
            "Skeletal Structure": "Vitruvian proportions and load paths",
        }
        self.anatomy_knowledge = {
            "Human Proportionality": "Vitruvian Man proportional canon",
            "Muscular Systems": "detailed musculature sheets",
            "Circulatory System": "venous and arterial mapping",
            "Body Mechanics": "posture, stance, and motion sequences",
        }

        self.models = {
            "Physics": FineTunedSLM("Physics", self.physics_knowledge),
            "Biomechanics": FineTunedSLM("Biomechanics", self.biomech_knowledge),
        }

        include_domain = include_domain.strip()
        if include_domain.lower() == "anatomy":
            self.models["Anatomy"] = FineTunedSLM("Anatomy", self.anatomy_knowledge)
        else:
            self.models[include_domain] = FineTunedSLM(include_domain, self.anatomy_knowledge)

    def extract_keywords(self, prompt: str) -> Dict[str, List[str]]:
        prompt_low = prompt.lower()
        result = {}
        for domain, model in self.models.items():
            kws = []
            for concept in model.knowledge.keys():
                parts = [p.strip() for p in concept.lower().replace("-", " ").split() if p.strip()]
                if any(p in prompt_low for p in parts):
                    kws.append(concept)
            result[domain] = sorted(set(kws))
        return result

    def generate_insights(self, prompt: str, keywords: Dict[str, List[str]]) -> Dict[str, str]:
        insights = {}
        for domain, model in self.models.items():
            insights[domain] = model.generate_insight(keywords.get(domain, []), user_prompt=prompt)
        return insights

    def synthesize_design(self, prompt: str, insights: Dict[str, str]) -> str:
        drivers = self._choose_drivers(insights)
        concept_name = self._propose_concept_name(drivers)
        
        lines = [
            f"# DVNC.ai — Innovation Report: Conceptual Product Prototype",
            f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            f"**Prompt Summary:** {prompt}",
            "",
            "## Multidisciplinary Insights",
        ]
        
        for domain in sorted(insights.keys()):
            lines.append(f"- **{domain}**: {insights[domain]}")

        lines.extend([
            "",
            "## Concept Synthesis",
            f"**Working Title:** {concept_name}",
            "",
            f"**Primary Drivers:** {', '.join(drivers)}",
            "",
            "### Concept Outline",
            "- **Architecture:** lightweight skeletal frame with modular joints.",
            "- **Propulsion/Actuation:** bio-inspired mechanism tuned via lever ratios.",
            "- **Control:** constraint-first controller (stability → efficiency → elegance).",
            "- **Materials:** prioritize high stiffness-to-weight; consider bio-derived composites.",
            "- **Validation:** benchtop test plan with 3 measurable KPIs from each domain.",
            "",
            "### MVP Test Matrix",
            "- **Physics:** lift/drag ratio target; static deflection under rated load.",
            "- **Biomechanics:** joint torque curve vs. desired motion; fatigue cycles.",
            "- **Anatomy:** proportionality adherence; ergonomic reach envelopes.",
            "",
            "### Next Steps",
            "1. Convert constraints to parametric CAD features.",
            "2. Build a breadboard prototype for force-path validation.",
            "3. Iterate with quick A/B experiments guided by the three SLMs.",
        ])
        
        return "\n".join(lines)

    def _choose_drivers(self, insights: Dict[str, str]) -> List[str]:
        import re
        drivers = []
        for txt in insights.values():
            bolds = re.findall(r"\*\*(.+?)\*\*", txt)
            if bolds:
                drivers.append(bolds[0])
        if not drivers:
            drivers = list(insights.keys())
        return drivers[:3]

    def _propose_concept_name(self, drivers: List[str]) -> str:
        nouns = [d.split()[-1] for d in drivers]
        return "Project " + "-".join(nouns).title()

# ---------- Chainlit Application ----------

# Initialize the system
dvnc_system: Optional[DVNCSystem] = None

@cl.on_chat_start
async def start():
    """Initialize the DVNC.ai system when a user connects."""
    global dvnc_system
    
    # Send welcome message with system description
    welcome_message = """
# 🎨 Welcome to DVNC.ai
## Leonardo's Intelligence, Reimagined for the 21st Century

I am a multi-disciplinary AI system inspired by Leonardo da Vinci's methodology of systematic, 
cross-domain observation. I integrate insights from:

- **Physics** (fluid dynamics, aerodynamics, mechanics, structures)
- **Biomechanics** (joints, muscles, biological levers, skeletal systems)  
- **Anatomy** (proportions, muscular systems, circulation, body mechanics)

### How to Use Me
Simply describe your engineering design challenge or complex problem, and I'll analyze it through 
Leonardo's multidisciplinary lens to generate innovative insights and conceptual prototypes.

### Example Prompts:
- "Design a compact rescue drone that can navigate narrow passages..."
- "Create a lightweight robotic manipulator optimized for reach and precision"
- "Develop a bio-inspired prosthetic limb with natural movement patterns"

**What engineering challenge would you like to explore today?**
"""
    
    await cl.Message(content=welcome_message).send()
    
    # Initialize the DVNC system
    dvnc_system = DVNCSystem(include_domain="Anatomy", seed=42)
    
    # Store in user session
    cl.user_session.set("dvnc_system", dvnc_system)
    
    # Send initialization status
    status_msg = "🔧 System initialized with Physics, Biomechanics, and Anatomy modules."
    await cl.Message(content=status_msg).send()

@cl.on_message
async def main(message: cl.Message):
    """Process user messages and generate DVNC.ai responses."""
    
    # Get the DVNC system from session
    dvnc_system = cl.user_session.get("dvnc_system")
    
    if not dvnc_system:
        await cl.Message(content="⚠️ System not initialized. Please refresh the page.").send()
        return
    
    # Get user prompt
    user_prompt = message.content
    
    # Send processing status
    processing_msg = cl.Message(content="🧭 Analyzing your prompt through Leonardo's multidisciplinary lens...")
    await processing_msg.send()
    
    # Extract keywords
    keywords = dvnc_system.extract_keywords(user_prompt)
    
    # Build keyword analysis message
    keyword_lines = ["### 📍 Keyword Extraction & Domain Routing"]
    for domain, kws in keywords.items():
        if kws:
            keyword_lines.append(f"- **{domain}:** {', '.join(kws)}")
        else:
            keyword_lines.append(f"- **{domain}:** —")
    
    await cl.Message(content="\n".join(keyword_lines)).send()
    
    # Generate insights
    insights_msg = cl.Message(content="💡 Generating domain-specific insights...")
    await insights_msg.send()
    
    insights = dvnc_system.generate_insights(user_prompt, keywords)
    
    # Build insights message
    insight_lines = ["### 🔬 Domain Expert Insights"]
    for domain, insight in sorted(insights.items()):
        insight_lines.append(f"\n**{domain} SLM:**")
        insight_lines.append(f"{insight}")
    
    await cl.Message(content="\n".join(insight_lines)).send()
    
    # Synthesize final design
    synthesis_msg = cl.Message(content="🎨 Synthesizing conceptual prototype...")
    await synthesis_msg.send()
    
    final_report = dvnc_system.synthesize_design(user_prompt, insights)
    
    # Send the final report
    await cl.Message(content=final_report).send()
    
    # Add follow-up prompt
    followup = """
---
### 🔄 Next Actions
- **Refine:** Provide more specific constraints or requirements
- **Explore:** Try a different design challenge
- **Deep Dive:** Ask about specific aspects of the proposed solution

*How would you like to proceed?*
"""
    await cl.Message(content=followup).send()

@cl.on_settings_update
async def setup_agent(settings):
    """Handle settings updates if needed."""
    pass

# Optional: Add custom actions
@cl.action_callback("regenerate")
async def on_action(action):
    """Handle regeneration requests."""
    await cl.Message(content="🔄 Regenerating analysis...").send()
    # Re-run the last prompt with different randomization
    pass

if __name__ == "__main__":
    # This would be run with: chainlit run dvnc_chainlit.py
    pass
