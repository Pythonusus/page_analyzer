from page_analyzer.app import index


def test_index():
    assert index() == 'Hello, World!'
