import cmd
import re
import shlex
import pynames
import inspect
from pynames import GENDER
from pynames import LANGUAGE

class NameGen(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.language = LANGUAGE.NATIVE
        self.races = ['elven', 'goblin', 'iron_kingdoms', 'korean', 
                'mongolian', 'orc', 'russian', 'scandinavian']
        self.genders = ['female', 'male']
        self.subclasses = {}
        for race in self.races:
            members = inspect.getmembers(getattr(pynames.generators, race))
            members = map(lambda x:x[0], members)
            members = list(filter(lambda x: 'Generator' in x and not 'From' in x, members))
            members = list(map(lambda x:re.sub('(Generator)|(Names)|(Fullname)', '', x), members))
            self.subclasses[race] = members
        languages = inspect.getmembers(LANGUAGE)
        languages = map(lambda x: x[0], languages)
        languages = filter(lambda x:x[0]!='_', languages)
        self.languages = list(languages)

    #generate
    def get_features(self, line:str, def_gender='male') -> tuple:
        keywords = shlex.split(line)
        race = keywords[0]
        gender = def_gender
        subclass = self.subclasses[race][0]
        if len(keywords) == 2:
            if keywords[1] in self.genders:
                gender = keywords[1]
            else:
                subclass = keywords[1]
        if len(keywords) == 3:
            subclass = keywords[1]
            gender = keywords[2]

        if gender == 'male':
            gender = GENDER.MALE
        elif gender == 'female':
            gender = GENDER.FEMALE
        return race, subclass, gender
    
    def get_gen_name(self, race, subclass):
        module = getattr(pynames.generators, race)
        members = inspect.getmembers(module)
        members = map(lambda x:x[0], members)
        members = [word for word in members if word.startswith(subclass)]
        return module, members[0]

    def get_language(self, gen):
        language = self.language
        if not language in gen.languages:
            language = LANGUAGE.NATIVE
        return language


    def do_generate(self, line:str) -> None:
        race, subclass, gender = self.get_features(line)
        module, generator_name = self.get_gen_name(race, subclass)
        gen = getattr(module, generator_name)()
        language = self.get_language(gen)
        name = gen.get_name_simple(gender, language)
        print(name)

    def complete_generate(self, prefix:str, line:str, begidx:int, endidx:int) -> list[str]:
        previous = line.split()[-2]
        if previous == 'generate':
            words = self.races
        elif previous in self.races and len(self.subclasses[previous]) > 1:
            words = self.subclasses[previous] + self.genders
        else:
            words = self.genders

        words = [word for word in words if word.lower().startswith(prefix.lower())]
        return words
    
    #language
    def do_language(self, line:str) -> None:
        self.language = getattr(LANGUAGE, line)

    def complete_language(self, prefix:str, *ignored) -> list[str]:
        return [word for word in self.languages if word.lower().startswith(prefix.lower())]

    #info
    def do_info(self, line:str) -> None:
        keywords = shlex.split(line)
        if keywords[-1] == 'language':
            race, subclass, _ = self.get_features(' '.join(keywords[:-1]))
            module, generator_name = self.get_gen_name(race, subclass)
            gen = getattr(module, generator_name)()
            print(*gen.languages)
        else:
            race, subclass, gender = self.get_features(line, '_')
            module, generator_name = self.get_gen_name(race, subclass)
            gen = getattr(module, generator_name)()
            attrs = []
            if gender != '_':
                attrs.append(gender)
            print(gen.get_names_number(*attrs))
        


    def complete_info(self, prefix:str, line:str, begidx:int, endidx:int) -> list[str]:
        previous = line.split()[-2]
        if previous == 'info':
            words = self.races
        elif previous in self.races and len(self.subclasses[previous]) > 1:
            words = self.subclasses[previous] + self.genders + ['language']
        else:
            words = self.genders + ['language']
        words = [word for word in words if word.lower().startswith(prefix.lower())]
        return words
        
        

    def do_EOF(self, line):
        print()
        return True

if __name__ == '__main__':
    NameGen().cmdloop()
