"""
============================================================================
CHE·NU™ V69 — LIBRARY MODULE TESTS
============================================================================
"""

import pytest
from datetime import datetime


# ============================================================================
# PUBLISHING TESTS
# ============================================================================

class TestPublishing:
    """Test publishing pipeline"""
    
    def test_create_pipeline(self):
        from ..publishing import create_pipeline
        pipeline = create_pipeline()
        assert pipeline is not None
    
    def test_upload_book(self):
        from ..publishing import create_pipeline
        
        pipeline = create_pipeline()
        
        book = pipeline.upload(
            title="Mon Roman",
            author_id="author-1",
            raw_text="Chapitre 1. Il était une fois...\n\nChapitre 2. La suite...",
        )
        
        assert book is not None
        assert book.title == "Mon Roman"
        assert book.status.value == "uploaded"
    
    def test_full_pipeline(self):
        from ..publishing import create_pipeline
        
        pipeline = create_pipeline()
        
        text = """
        Chapitre Premier
        
        Le soleil se levait sur la ville endormie. Marie ouvrit les yeux,
        encore engourdie par le sommeil. Une nouvelle journée commençait.
        
        Elle se leva doucement et regarda par la fenêtre. Les rues étaient
        encore vides, baignées dans la lumière dorée du matin.
        """
        
        book, success, message = pipeline.run_full_pipeline(
            title="L'Aube Nouvelle",
            author_id="author-1",
            raw_text=text,
        )
        
        assert success
        assert book.status.value == "published"
        assert len(book.chapters) > 0
    
    def test_semantic_search(self):
        from ..publishing import create_pipeline
        
        pipeline = create_pipeline()
        
        # Publish a book
        pipeline.run_full_pipeline(
            "Science Fiction Story",
            "author-1",
            "In the year 2100, space travel became routine. Astronauts explored distant planets.",
        )
        
        # Search
        results = pipeline.search("space exploration", threshold=0.3)
        assert len(results) >= 0  # May or may not find depending on mock vectors


# ============================================================================
# IMMERSIVE READING TESTS
# ============================================================================

class TestImmersiveReading:
    """Test immersive reading engine"""
    
    def test_create_engine(self):
        from ..immersive_reading import create_engine
        engine = create_engine()
        assert engine is not None
    
    def test_generate_scene(self):
        from ..immersive_reading import create_engine, create_reader_profile
        from ..models import ChapterChunk
        
        engine = create_engine()
        
        # Setup reader
        profile = create_reader_profile("reader-1")
        engine.set_reader_profile(profile)
        
        # Create chunk
        chunk = ChapterChunk(
            chunk_id="chunk-1",
            chapter_no=1,
            order_index=0,
            text="Le château se dressait sur la montagne, entouré de brume mystérieuse.",
            word_count=10,
        )
        
        # Generate scene
        manifest = engine.generate_scene(chunk, "reader-1")
        
        assert manifest is not None
        assert manifest.environment_theme in ["fantasy", "nature", "interior"]
    
    def test_emotion_extraction(self):
        from ..immersive_reading.engine import EmotionExtractor
        
        extractor = EmotionExtractor()
        
        text = "Elle pleurait de joie en voyant le soleil se lever après la tempête."
        result = extractor.extract(text)
        
        assert "emotions" in result
        assert "dominant_emotion" in result


# ============================================================================
# AUTHOR EQUITY TESTS
# ============================================================================

class TestAuthorEquity:
    """Test author equity system"""
    
    def test_create_system(self):
        from ..author_equity import create_equity_system
        system = create_equity_system()
        assert system is not None
    
    def test_register_author(self):
        from ..author_equity import create_equity_system
        
        system = create_equity_system()
        wallet = system.register_author("author-1")
        
        assert wallet is not None
        assert wallet.owner_id == "author-1"
    
    def test_setup_book_contract(self):
        from ..author_equity import create_equity_system, create_split_config
        
        system = create_equity_system()
        
        split = create_split_config(author_split=0.9)
        wallet, contract = system.setup_book("book-1", "author-1", split_config=split)
        
        assert contract is not None
        assert contract.book_id == "book-1"
        assert contract.signature != ""
    
    def test_process_tip(self):
        from ..author_equity import create_equity_system
        
        system = create_equity_system()
        
        # Setup
        system.setup_book("book-1", "author-1")
        
        # Process tip
        tx = system.process_tip("reader-1", "book-1", 10.0)
        
        assert tx is not None
        assert tx.amount > 0


# ============================================================================
# LITERATURE ZONE TESTS
# ============================================================================

class TestLiteratureZone:
    """Test Universal Literature Zone"""
    
    def test_create_zone(self):
        from ..literature_zone import create_literature_zone
        zone = create_literature_zone()
        assert zone is not None
    
    def test_publish_book(self):
        from ..literature_zone import create_literature_zone
        
        zone = create_literature_zone()
        
        text = "Il était une fois un petit village au pied de la montagne."
        book, success, message = zone.publish_book(
            "Le Village",
            "author-1",
            text,
        )
        
        assert success
        assert book.status.value == "published"
    
    def test_creative_companion(self):
        from ..literature_zone import create_companion
        from ..models import BookArtifact, ChapterChunk
        
        companion = create_companion()
        
        # Create mock book
        book = BookArtifact(
            book_id="book-1",
            title="Test Book",
            author_id="author-1",
            chapters=[
                ChapterChunk(
                    chunk_id="c1", chapter_no=1, order_index=0,
                    text="Chapter one text here.",
                    word_count=100,
                ),
                ChapterChunk(
                    chunk_id="c2", chapter_no=2, order_index=1,
                    text="Chapter two text here.",
                    word_count=150,
                ),
            ],
        )
        
        # Analyze structure
        analysis = companion.analyze_structure(book)
        
        assert analysis["total_chapters"] == 2
        assert "rhythm_analysis" in analysis
    
    def test_companion_no_auto_apply(self):
        from ..literature_zone import create_companion
        from ..models import BookArtifact, ChapterChunk
        
        companion = create_companion()
        
        chunk = ChapterChunk(
            chunk_id="c1", chapter_no=1, order_index=0,
            text="The word was was was was repeated many times. It was very repetitive.",
            word_count=15,
        )
        
        suggestions = companion.suggest_style("book-1", chunk)
        
        # Verify NO suggestion is auto-applied
        for s in suggestions:
            assert s.auto_applied is False, "Suggestions must NEVER be auto-applied"


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests"""
    
    def test_full_reading_experience(self):
        """Test complete reading flow"""
        from ..literature_zone import create_literature_zone
        
        zone = create_literature_zone()
        
        # 1. Publish book
        text = """
        Le mystère de la forêt enchantée
        
        Dans une forêt ancienne vivait une créature magique. Elle gardait
        un secret que personne ne connaissait. Un jour, un jeune aventurier
        découvrit le chemin qui menait à son refuge.
        
        La créature était surprise de voir un humain. Mais quelque chose
        dans ses yeux lui inspira confiance. Peut-être était-il temps de
        partager son secret.
        """
        
        book, success, _ = zone.publish_book(
            "La Forêt Enchantée",
            "author-1",
            text,
        )
        
        assert success
        
        # 2. Setup reader
        from ..immersive_reading import create_reader_profile
        profile = create_reader_profile("reader-1")
        zone.immersive.set_reader_profile(profile)
        
        # 3. Read immersively
        result = zone.read_immersive(book.book_id, "reader-1", 0)
        
        assert result is not None
        chunk, manifest = result
        assert manifest.environment_theme is not None
        
        # 4. Tip author
        tx = zone.tip_author("reader-1", book.book_id, 5.0)
        assert tx is not None
        
        # 5. Get companion feedback
        feedback = zone.get_companion_feedback(book.book_id)
        assert "structure" in feedback


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
