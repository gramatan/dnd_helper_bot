from dataclasses import dataclass

@dataclass
class SpellCard:
    title: str
    title_en: str
    link: str
    level: str
    school: str
    level_school: str = None
    casting_time: str = None
    c_range: str = None
    components: str = None
    duration: str = None
    classes: str = None
    archetypes: str = None
    source: str = None
    description: str = None
