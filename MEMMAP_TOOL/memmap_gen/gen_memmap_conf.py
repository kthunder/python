from itertools import product
from pprint import pprint

DEFAULT_CONFIG = {
    # Default behavior:
    # UPPERCASE is MACRO name, its lowercase is section name
    "general_fields": {
        "init_policy": [
            "INIT",
            "CLEARED"
            # dict(macro="CLEARED", section="bss")
        ],
        "align": [
            "BOOLEAN",
            "8",
            "16",
            "32",
            "PTR",
            "UNSPECIFIED"
        ],
    },
    "templates": [
        # catagory: VAR
        {
            "macro_name": [
                dict(macro="VAR", section="data"),
                dict(macro="VAR_FAST", section="data_fast"),
            ],
            "physical_area": {
                'default': "data",
                'INIT': "data",
                "CLEARED": "bss"
            },
            "use_fields": ["init_policy", "align"],
            "macro_template": "{macro_name}_{init_policy}_{align}",
            "section_template": ".mcal_{macro_name}_{init_policy}_{align}",
        },
        # catagory: CONST
        {
            "macro_name": [
                "CONST",
                "CONST_FAST"
            ],
            "use_fields": ["align"],
            "physical_area": {'default': "rodata"},
            "macro_template": "{macro_name}_{align}",
            "section_template": ".mcal_{macro_name}_{align}",
        },
        # catagory: CONFIG_DATA
        {
            "macro_name": [
                "CONFIG_DATA"
            ],
            "physical_area": {'default': "rodata"},
            "use_fields": ["align"],
            "macro_template": "{macro_name}_{align}",
            "section_template": ".mcal_{macro_name}_{align}",
        },
        # catagory: CODE
        {
            "macro_name": [
                dict(macro="CODE", section="text_normal"),
                dict(macro="CODE_FAST", section="text_fast"),
                dict(macro="CODE_SLOW", section="text_slow"),
            ],
            "physical_area": {'default': "text"},
            "macro_template": "{macro_name}",
            "section_template": ".mcal_{macro_name}",
        },
    ]
}


def default_dict(default_dict, update_dict):
    '''
    更新字典
    '''
    result_dict = default_dict.copy()
    result_dict.update(update_dict)
    return result_dict


def expand_macro_section(list_items):
    '''
    扩充属性字段（宏字段和段字段）
    '''
    # print("expand_macro_section >>>>>>>>")
    # print(f"list_items : {list_items}")
    result_list = []
    for v in list_items:
        # print(f"v : {v}")
        result_list.append(
            dict(macro=v.upper(), section=v.lower()) if isinstance(v, str) else v)
    # print(f"result_list {result_list}")
    # print("expand_macro_section <<<<<<<<\n")
    return result_list


def gen_memmap_config_lines():
    # Construct fields
    fields = DEFAULT_CONFIG['general_fields']
    for k, v_list in fields.copy().items():
        # print(f"fields[k] before : {fields[k]}")
        fields[k] = expand_macro_section(v_list)
        # print(f"fields[k] after  : {fields[k]}")
    templates = DEFAULT_CONFIG['templates']
    default_template_dict = {
        "macro_name": "",
        "physical_area": "",
        "use_fields": [],
        "macro_template": "",
        "section_template": "",
    }
    # Generate templates
    for template in templates:
        # print(template)
        # if template['macro_name'][0]['macro'].find('VAR') != -1:
        #     print(template)
        template = default_dict(default_template_dict, template)
        fields_namelist = list(template['use_fields'])
        # pprint(fields_namelist)
        # pprint(fields)
        product_fields = [expand_macro_section(
            template['macro_name'])] + [fields[field] for field in fields_namelist]
        # 当前模板的笛卡尔积
        field_info_all = [dict(list(zip(['macro_name'] + fields_namelist, f)))
                          for f in product(*product_fields)]
        for field_info in field_info_all:
            macro_info = {k: v['macro'] for k, v in field_info.items()}
            section_info = {k: v['section'] for k, v in field_info.items()}
            macro = template['macro_template'].format(**macro_info)
            # 特殊处理VAR的pyh，包含data和bss两种选项
            phy = template["physical_area"][macro_info.get(
                "init_policy", "default")]
            section = template['section_template'].format(**section_info)
            print(f'{macro:40},{phy:10},{section:30}')
            yield f'{macro},{phy},{section}'


if __name__ == '__main__':
    lines = gen_memmap_config_lines()
    with open("MmeMapConfig.csv", "w+") as f:
        f.writelines([line + '\n' for line in lines])
    for line in lines:
        print(line)
