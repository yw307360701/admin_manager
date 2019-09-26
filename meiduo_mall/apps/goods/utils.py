

def get_breadcrumb(cat3):
    """包装面包屑导航"""
    cat1 = cat3.parent.parent
    cat1.url = cat1.goodschannel_set.all()[0].url

    breadcrumb = {
        'cat1': cat1,
        'cat2': cat3.parent,
        'cat3': cat3
    }

    return breadcrumb