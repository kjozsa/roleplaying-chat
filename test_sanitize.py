from app import sanitize


def test_sanitize():
    assert '' == sanitize('')
    assert '' == sanitize('((a)')
    assert '(' == sanitize('(')
    assert 'qwertyui' == sanitize('qwertyui')
    assert 'qwertyui ' == sanitize('qwertyui (abcdef)')
    assert 'qwertyui  poiuy' == sanitize('qwertyui (abcdef) poiuy')

    assert '"Teacher, I heard about a fascinating story from someone who lives in the city. Can you guess who it might be?" ' == sanitize('"Teacher, I heard about a fascinating story from someone who lives in the city. Can you guess who it might be?" (I want to find out if the Teacher can make any connections between my statement and their own information.)')
