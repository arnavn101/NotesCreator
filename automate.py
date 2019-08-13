import core
core_module = core.Text2Speech(8,"lesson.txt")

import converter
converter.convert("lesson.txt")

import summarizer
summarizer.generate_summary("lesson.txt", 3)
