import glob
import os.path
from collections import OrderedDict

import xmltodict
import javalang
import pygments
from pygments.lexers import JavaLexer
from pygments.token import Token


class BugReport:
    """Class representing each bug report"""

    __slots__ = ['summary', 'description', 'fixed_files', 'opendate', 'fixdate',
                 'pos_tagged_summary', 'pos_tagged_description', 'stack_traces']

    def __init__(self, summary, description, fixed_files, opendate, fixdate,):
        self.summary = summary
        self.description = description
        self.fixed_files = fixed_files
        self.opendate = opendate
        self.fixdate = fixdate
        self.pos_tagged_summary = None
        self.pos_tagged_description = None
        self.stack_traces = None


class SourceFile:
    """Class representing each source file"""

    __slots__ = ['all_content', 'comments', 'comments_hub', 'class_names', 'class_names_hub', 'attributes', 'attributes_hub',
                 'method_names', 'method_names_hub', 'variables', 'variables_hub', 'file_name', 'pos_tagged_comments',
                 'exact_file_name', 'package_name', 'class_imports']

    def __init__(self, all_content, comments, comments_hub, class_names, class_names_hub, attributes, attributes_hub,
                 method_names, method_names_hub,variables, variables_hub, file_name, package_name, class_imports):
        self.all_content = all_content  # chứa tất cả nội dung code
        self.comments = comments  # comments
        self.comments_hub = comments_hub  # comments
        self.class_names = class_names
        self.class_names_hub = class_names_hub
        self.attributes = attributes
        self.attributes_hub = attributes_hub
        self.method_names = method_names
        self.method_names_hub = method_names_hub
        self.variables = variables
        self.variables_hub = variables_hub
        self.file_name = file_name
        self.exact_file_name = file_name[0]
        self.package_name = package_name
        self.pos_tagged_comments = None
        self.class_imports = class_imports

class Parser:
    """Class containing different parsers"""

    __slots__ = ['name', 'src', 'bug_repo']

    def __init__(self, project):
        self.name = project.name
        self.src = project.src
        self.bug_repo = project.bug_repo

    def report_parser(self):
        """Parse XML format bug reports"""

        # Convert XML bug repository to a dictionary
        with open(self.bug_repo) as xml_file:
            xml_dict = xmltodict.parse(
                xml_file.read(), force_list={'file': True})

        # Iterate through bug reports and build their objects
        bug_reports = OrderedDict()

        for bug_report in xml_dict['bugrepository']['bug']:
            bug_reports[bug_report['@id']] = BugReport(
                bug_report['buginformation']['summary'],
                bug_report['buginformation']['description']
                if bug_report['buginformation']['description'] else '',
                [os.path.normpath(path)
                 for path in bug_report['fixedFiles']['file']],
                bug_report['@opendate'],
                bug_report['@fixdate'],
            )

        return bug_reports

    def src_parser(self):
        """Parse source code directory of a program and collect
        its java files.
        """

        # Getting the list of source files recursively from the source directory
        src_addresses = glob.glob(str(self.src) + '/**/*.java', recursive=True)

        # Creating a java lexer instance for pygments.lex() method
        java_lexer = JavaLexer()

        src_files = OrderedDict()

        # Looping to parse each source file
        for src_file in src_addresses:
            with open(src_file) as file:
                src = file.read()

            # Placeholder for different parts of a source file
            comments = ''
            comments_hub = ''
            class_names = []
            class_names_hub = []
            attributes = []
            attributes_hub = []
            method_names = []
            method_names_hub = []
            variables = []
            variables_hub = []
            class_imports = []
            # print([os.path.basename(src_file).split('.')[0]])
            # Source parsing
            parse_tree = None
            try:
                parse_tree = javalang.parse.parse(src)
                for path, node in parse_tree.filter(javalang.tree.VariableDeclarator):
                    if isinstance(path[-2], javalang.tree.FieldDeclaration):
                        attributes.append(node.name)
                        attributes_hub.append(node.name)
                    elif isinstance(path[-2], javalang.tree.VariableDeclaration):
                        variables.append(node.name)
                        variables_hub.append(node.name)
            except:
                pass

            # Trimming the source file
            ind = False
            if parse_tree:
                if parse_tree.imports:
                    last_imp_path = parse_tree.imports[-1].path
                    src = src[src.index(last_imp_path) +
                              len(last_imp_path) + 1:]
                elif parse_tree.package:
                    package_name = parse_tree.package.name
                    src = src[src.index(package_name) + len(package_name) + 1:]
                else:  # There is no import and no package declaration
                    ind = True
            # javalang can't parse the source file
            else:
                ind = True

            # Lexically tokenize the source file
            lexed_src = pygments.lex(src, java_lexer)
            # src__ = []
            # for token in lexed_src:
            #     src__.append(token)
            # for i, token in enumerate(src__):
            #     if token[0] is Token.Name and src__[i + 1][0] is Token.Text and src__[i + 2][0] is Token.Name:
            #         # print(token[1])
            #         class_imports.append(token[1])
            for i, token in enumerate(lexed_src):
                if token[0] in Token.Comment:
                    if ind and i == 0 and token[0] is Token.Comment.Multiline:
                        src = src[src.index(token[1]) + len(token[1]):]
                        continue
                    comments += token[1]
                    comments_hub += token[1]
                elif token[0] is Token.Name.Class:
                    class_names.append(token[1])
                    class_names_hub.append(token[1])
                elif token[0] is Token.Name.Function:
                    method_names.append(token[1])
                    method_names_hub.append(token[1])

            # Get the package declaration if exists
            if parse_tree and parse_tree.package:
                package_name = parse_tree.package.name
            else:
                package_name = None

            if self.name == 'aspectj':
                src_files[os.path.relpath(src_file, start=self.src)] = SourceFile(
                    src, comments, comments_hub, class_names, class_names_hub, attributes, attributes_hub,
                    method_names, method_names_hub, variables, variables_hub,
                    [os.path.basename(src_file).split('.')[0]],
                    package_name, class_imports
                )
            else:
                # If source file has package declaration
                if package_name:
                    src_id = (package_name + '.' +
                              os.path.basename(src_file))
                else:
                    src_id = os.path.basename(src_file)

                src_files[src_id] = SourceFile(
                    src, comments, comments_hub, class_names, class_names_hub, attributes, attributes_hub,
                    method_names, method_names_hub, variables, variables_hub,
                    [os.path.basename(src_file).split('.')[0]],
                    package_name, class_imports
                )
        return src_files


def test():
    import datasets

    parser = Parser(datasets.zxing)
    x = parser.report_parser()
    d = parser.src_parser()

    src_id, src = list(d.items())[10]
    print(src_id, src.exact_file_name, src.package_name)


if __name__ == '__main__':
    test()
