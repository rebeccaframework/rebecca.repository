""" pyramid config directives
"""

from .interfaces import IRepository

def includeme(config):
    config.add_directive('add_repository', add_repository)


def add_repository(config, repository, name):
    reg = config.registry
    repository = config.maybe_dotted(repository)

    def register():
        reg.registerUtility(repository, IRepository, name=name)

    desc = "rebecca.repository:{name}".format(name=name)
    intr = config.introspectable(category_name="rebecca.repository",
                                 discriminator=name,
                                 title=desc,
                                 type_name=repository.__class__.__name__)
    intr['value'] = repository
    config.action(desc,
                  register, introspectables=(intr,))
