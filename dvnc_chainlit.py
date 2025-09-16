#!/usr/bin/env python3
"""
DVNC.ai – Premium Chainlit Integration
Leonardo da Vinci-inspired AI System with Enhanced UI/UX
"""

import chainlit as cl
import random
import asyncio
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

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
            "Fractal Geometry": "tree branching and river delta patterns",
            "Wave Propagation": "sound and light behavior studies",
        }
        self.biomech_knowledge = {
            "Joint Articulation": "elbow/shoulder motion notebooks",
            "Muscular Force": "layered muscle drawings",
            "Biological Levers": "limb lever ratios and gait notes",
            "Skeletal Structure": "Vitruvian proportions and load paths",
            "Kinematic Chains": "sequential movement studies",
            "Energy Transfer": "force distribution in living systems",
        }
        self.anatomy_knowledge = {
            "Human Proportionality": "Vitruvian Man proportional canon",
            "Muscular Systems": "detailed musculature sheets",
            "Circulatory System": "venous and arterial mapping",
            "Body Mechanics": "posture, stance, and motion sequences",
            "Neural Pathways": "brain and nerve studies",
            "Sensory Integration": "eye and ear mechanism drawings",
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

    def synthesize_design(self, prompt: str, insights: Dict[str, str]) -> List[str]:
        """Returns design synthesis as a list of sections for streaming"""
        drivers = self._choose_drivers(insights)
        concept_name = self._propose_concept_name(drivers)
        
        sections = []
        
        # Header section
        header = [
            "# 🎨 DVNC.ai — Innovation Report",
            f"*Conceptual Product Prototype*",
            "",
            f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Challenge:** {prompt}",
            ""
        ]
        sections.append("\n".join(header))
        
        # Insights section
        insights_lines = ["## 🔬 Multidisciplinary Insights\n"]
        for domain in sorted(insights.keys()):
            domain_icon = self._get_domain_icon(domain)
            insights_lines.append(f"### {domain_icon} {domain}")
            insights_lines.append(f"{insights[domain]}\n")
        sections.append("\n".join(insights_lines))
        
        # Synthesis section
        synthesis = [
            "## 🚀 Concept Synthesis",
            f"### **{concept_name}**",
            "",
            f"**Primary Innovation Drivers:** `{' × '.join(drivers)}`",
            ""
        ]
        sections.append("\n".join(synthesis))
        
        # Architecture section
        architecture = [
            "### 📐 System Architecture",
            "",
            "#### Structural Framework",
            "- **Core Structure:** Lightweight skeletal frame with modular joints",
            "- **Material Strategy:** High stiffness-to-weight ratio composites",
            "- **Modularity:** Interchangeable components for rapid iteration",
            "",
            "#### Actuation System",
            "- **Primary Motion:** Bio-inspired mechanism with optimized lever ratios",
            "- **Control Logic:** Constraint-first controller (stability → efficiency → elegance)",
            "- **Power Distribution:** Distributed energy management system",
            ""
        ]
        sections.append("\n".join(architecture))
        
        # Validation section
        validation = [
            "### 🧪 Validation Framework",
            "",
            "#### Performance Metrics",
            "| Domain | Key Performance Indicator | Target | Test Method |",
            "|--------|--------------------------|--------|-------------|",
            "| **Physics** | Lift/drag ratio | >3.5 | Wind tunnel testing |",
            "| **Physics** | Structural deflection | <5mm @ rated load | Static load test |",
            "| **Biomechanics** | Joint torque efficiency | >85% | Dynamometer analysis |",
            "| **Biomechanics** | Fatigue resistance | >10,000 cycles | Cyclic loading |",
            "| **Anatomy** | Ergonomic compliance | >90% user satisfaction | User studies |",
            "| **Anatomy** | Proportional accuracy | ±2% of target | 3D scanning |",
            ""
        ]
        sections.append("\n".join(validation))
        
        # Implementation roadmap
        roadmap = [
            "### 🗺️ Implementation Roadmap",
            "",
            "#### Phase 1: Proof of Concept (Weeks 1-4)",
            "- [ ] Convert constraints to parametric CAD model",
            "- [ ] Develop initial control algorithms",
            "- [ ] Create simulation environment",
            "",
            "#### Phase 2: Prototype Development (Weeks 5-8)",
            "- [ ] Build physical breadboard prototype",
            "- [ ] Implement sensor feedback systems",
            "- [ ] Conduct initial performance tests",
            "",
            "#### Phase 3: Iteration & Optimization (Weeks 9-12)",
            "- [ ] A/B testing with design variants",
            "- [ ] Machine learning optimization of control parameters",
            "- [ ] User testing and feedback integration",
            "",
            "---",
            "*Powered by Leonardo da Vinci's timeless principles of observation and innovation*"
        ]
        sections.append("\n".join(roadmap))
        
        return sections

    def _get_domain_icon(self, domain: str) -> str:
        icons = {
            "Physics": "⚛️",
            "Biomechanics": "🦾",
            "Anatomy": "🫀"
        }
        return icons.get(domain, "🔬")

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

# ---------- Chat History Management ----------

class ChatHistory:
    def __init__(self):
        self.history = []
        self.max_history = 50
        
    def add_interaction(self, user_input: str, assistant_response: str):
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "assistant": assistant_response
        })
        # Keep only last N interactions
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_recent(self, n: int = 5) -> List[Dict]:
        return self.history[-n:] if self.history else []
    
    def clear(self):
        self.history = []

# ---------- Chainlit Application ----------

# Initialize the system
dvnc_system: Optional[DVNCSystem] = None
chat_history: Optional[ChatHistory] = None

@cl.on_chat_start
async def start():
    """Initialize the DVNC.ai system when a user connects."""
    global dvnc_system, chat_history
    
    # Set custom avatar for the assistant
    await cl.Avatar(
        name="DVNC.ai",
        url="https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Artist%20palette/Color/artist_palette_color.svg"
    ).send()
    
    # Send animated welcome message
    welcome_parts = [
        "# 🎨 DVNC.ai",
        "## *Leonardo's Intelligence, Reimagined for the 21st Century*",
        "",
        "Welcome to a revolutionary AI system that channels Leonardo da Vinci's genius "
        "to solve modern engineering challenges.",
        "",
        "### 🧠 My Capabilities:",
        "- **Multi-Domain Analysis**: Physics, Biomechanics, and Anatomy",
        "- **Cross-Disciplinary Innovation**: Connecting insights across domains",
        "- **Da Vinci Methodology**: Systematic observation and radical creativity",
        "",
        "### 💡 Example Challenges:",
        "```",
        "• Design a bio-inspired underwater drone",
        "• Create an adaptive prosthetic limb",
        "• Develop a shape-shifting rescue robot",
        "• Engineer a self-healing material system",
        "```",
        "",
        "---",
        "*What engineering challenge shall we explore together?*"
    ]
    
    # Stream the welcome message
    msg = cl.Message(content="")
    await msg.send()
    
    for part in welcome_parts:
        await asyncio.sleep(0.05)  # Small delay for streaming effect
        msg.content += part + "\n"
        await msg.update()
    
    # Initialize the DVNC system
    dvnc_system = DVNCSystem(include_domain="Anatomy", seed=42)
    chat_history = ChatHistory()
    
    # Store in user session
    cl.user_session.set("dvnc_system", dvnc_system)
    cl.user_session.set("chat_history", chat_history)
    
    # Add action buttons
    actions = [
        cl.Action(name="clear_history", value="clear", description="Clear Chat History"),
        cl.Action(name="show_history", value="show", description="Show Recent History"),
        cl.Action(name="export_report", value="export", description="Export Last Report"),
    ]
    msg.actions = actions
    await msg.update()

@cl.on_message
async def main(message: cl.Message):
    """Process user messages and generate DVNC.ai responses."""
    
    # Get the DVNC system and history from session
    dvnc_system = cl.user_session.get("dvnc_system")
    chat_history = cl.user_session.get("chat_history")
    
    if not dvnc_system:
        await cl.Message(content="⚠️ System not initialized. Please refresh the page.").send()
        return
    
    # Get user prompt
    user_prompt = message.content
    
    # Initialize response message for streaming
    response_msg = cl.Message(content="")
    await response_msg.send()
    
    # Stage 1: Processing indicator with animation
    processing_frames = [
        "🔬 Analyzing your challenge",
        "🔬 Analyzing your challenge.",
        "🔬 Analyzing your challenge..",
        "🔬 Analyzing your challenge..."
    ]
    
    for frame in processing_frames:
        response_msg.content = frame
        await response_msg.update()
        await asyncio.sleep(0.2)
    
    # Stage 2: Extract keywords with streaming
    response_msg.content = "### 📍 Domain Analysis\n\n"
    await response_msg.update()
    
    keywords = dvnc_system.extract_keywords(user_prompt)
    
    # Stream keyword analysis
    for domain, kws in keywords.items():
        icon = dvnc_system._get_domain_icon(domain)
        domain_text = f"**{icon} {domain}:** "
        if kws:
            domain_text += f"`{' • '.join(kws)}`\n"
        else:
            domain_text += "*No specific concepts detected*\n"
        
        response_msg.content += domain_text
        await response_msg.update()
        await asyncio.sleep(0.1)
    
    response_msg.content += "\n---\n"
    await response_msg.update()
    
    # Stage 3: Generate insights with streaming
    response_msg.content += "### 💡 Generating Domain Insights\n\n"
    await response_msg.update()
    
    insights = dvnc_system.generate_insights(user_prompt, keywords)
    
    # Stream each insight
    for domain, insight in sorted(insights.items()):
        icon = dvnc_system._get_domain_icon(domain)
        
        # Stream domain header
        response_msg.content += f"**{icon} {domain} Analysis:**\n"
        await response_msg.update()
        await asyncio.sleep(0.1)
        
        # Stream insight text word by word for effect
        words = insight.split()
        line = ""
        for i, word in enumerate(words):
            line += word + " "
            if i % 5 == 4:  # Update every 5 words
                response_msg.content += line
                await response_msg.update()
                line = ""
                await asyncio.sleep(0.05)
        
        if line:  # Add remaining words
            response_msg.content += line
            await response_msg.update()
        
        response_msg.content += "\n\n"
        await response_msg.update()
    
    response_msg.content += "---\n"
    await response_msg.update()
    
    # Stage 4: Synthesize design with section streaming
    response_msg.content += "\n"
    await response_msg.update()
    
    design_sections = dvnc_system.synthesize_design(user_prompt, insights)
    
    # Stream each section
    for section in design_sections:
        # Add section with streaming effect
        lines = section.split('\n')
        for line in lines:
            response_msg.content += line + "\n"
            await response_msg.update()
            await asyncio.sleep(0.02)  # Very short delay for smooth streaming
        
        await asyncio.sleep(0.1)  # Pause between sections
    
    # Save to history
    full_response = response_msg.content
    chat_history.add_interaction(user_prompt, full_response)
    
    # Add action buttons to the response
    actions = [
        cl.Action(
            name="regenerate",
            value=user_prompt,
            description="🔄 Regenerate Analysis"
        ),
        cl.Action(
            name="save_report",
            value=full_response,
            description="💾 Save Report"
        ),
    ]
    response_msg.actions = actions
    await response_msg.update()

@cl.action_callback("regenerate")
async def on_regenerate(action: cl.Action):
    """Handle regeneration requests."""
    # Re-seed the system for different results
    dvnc_system = cl.user_session.get("dvnc_system")
    dvnc_system.__init__(include_domain="Anatomy", seed=random.randint(1, 1000))
    
    # Create a new message with the original prompt
    await cl.Message(content=f"🔄 Regenerating analysis for: *{action.value}*").send()
    
    # Trigger the main handler with the original prompt
    mock_message = cl.Message(content=action.value)
    await main(mock_message)

@cl.action_callback("clear_history")
async def on_clear_history(action: cl.Action):
    """Clear chat history."""
    chat_history = cl.user_session.get("chat_history")
    chat_history.clear()
    await cl.Message(content="✨ Chat history cleared.").send()

@cl.action_callback("show_history")
async def on_show_history(action: cl.Action):
    """Show recent chat history."""
    chat_history = cl.user_session.get("chat_history")
    recent = chat_history.get_recent(5)
    
    if not recent:
        await cl.Message(content="📭 No chat history available.").send()
        return
    
    history_msg = "### 📜 Recent Conversations\n\n"
    for i, item in enumerate(recent, 1):
        timestamp = datetime.fromisoformat(item["timestamp"]).strftime("%H:%M:%S")
        history_msg += f"**[{timestamp}] Query {i}:**\n"
        history_msg += f"_{item['user'][:100]}..._\n\n"
    
    await cl.Message(content=history_msg).send()

@cl.action_callback("save_report")
async def on_save_report(action: cl.Action):
    """Save report as file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"dvnc_report_{timestamp}.md"
    
    # Create file element
    elements = [
        cl.File(
            name=filename,
            content=action.value.encode(),
            display="inline",
        )
    ]
    
    await cl.Message(
        content=f"📄 Report saved as `{filename}`",
        elements=elements
    ).send()

@cl.on_settings_update
async def setup_agent(settings):
    """Handle settings updates if needed."""
    pass

if __name__ == "__main__":
    # This would be run with: chainlit run dvnc_chainlit.py -w
    pass
