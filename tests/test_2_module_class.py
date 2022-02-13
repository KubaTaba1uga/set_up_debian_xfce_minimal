def test_sorted_scripts(module):
    script_list = module._list_sorted_scripts()
    for i, script in enumerate(module):
        assert script.name.find_script_number() == script_list[i][0]
