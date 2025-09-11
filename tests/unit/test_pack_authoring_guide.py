from pathlib import Path

from rulebook_ai.community_packs import validate_pack_structure


def test_pack_authoring_guide_is_valid():
    pack_path = Path('src/rulebook_ai/packs/pack-authoring-guide')
    name, manifest = validate_pack_structure(pack_path)
    assert name == 'pack-authoring-guide'
    assert manifest['version'] == '0.1.0'
