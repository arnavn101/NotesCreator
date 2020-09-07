import os
import sys
import textract
from summarize_text import summarizer
from analyze_tone import tone_analysis
from article_scraper import scrape_articles
from processAudio import convert_audio, audio_preprocessing
from utils import progress_bar, puncutate_text, delete_useless
sys.path.insert(0, os.getcwd())  # Resolve Importing errors


class ManageTask:
    def __init__(self, **kwargs):
        self.file_path = os.path.join('downloads', 'scraped_text.txt')
        if kwargs.get("function_identifier") == "notes":
            self.initialize_notes(**kwargs)
            retrieve_summary = summarizer.Summarizer(self.file_path, int(kwargs.get("bullet_points")))
            self.final_text = (retrieve_summary.return_summary()).splitlines()
        elif kwargs.get("function_identifier") == "tone_analyze":
            self.initialize_toneAnalysis(**kwargs)
        delete_useless.execute()

    def initialize_notes(self, **kwargs):
        if kwargs.get("operation_choice") == "Website":
            scraping_articles = scrape_articles.ArticleScraper(kwargs.get("specified_url"))
            self.write_file(self.file_path, scraping_articles.return_article())
        elif kwargs.get("operation_choice") == "Attachment":
            if kwargs.get("minor_operation") == "valid_extensions":
                text_document = textract.process(kwargs.get("file_path"))
                text_document = text_document.decode('utf8').encode('ascii', errors='ignore')
                text_document = text_document.replace(b"\n", b" ")
                text_document = text_document.replace(b"\t", b" ")
                self.write_file(self.file_path, str(text_document))
            elif kwargs.get("minor_operation") == "invalid_extensions":
                audio_preprocessing.PreProcessor()
                convert_audio.Text2Speech(5, self.file_path)
                puncutate_text.convert_text(self.file_path)

    def initialize_toneAnalysis(self, **kwargs):
        toneAnalyzer = tone_analysis.Tone_Analysis(kwargs.get("text_required"))
        self.final_text = ((toneAnalyzer.finale()).splitlines())

    # Writing contents of response to file
    def write_file(self, file_name, content):
        with open(file_name, 'w+', encoding='utf-8') as file:
            file.write(content)

    def return_text(self):
        return self.final_text
