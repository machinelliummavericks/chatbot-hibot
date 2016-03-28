import xml.etree.ElementTree as ET
import os
import re
import string

def remove_tags(aiml_file, dir_in, dir_out):
    """ Remove tags from original AIML files and write new files

        :param aiml_file: AIML file name
        :param dir_in: directory where input AIML files are location
        :param aiml_file: directory to write tag free AIML files too

        :example:
            Original AIML ==>
            <category><pattern>WHERE IS VENUS</pattern>
            <template><set name="it"><set name="topic"> VENUS </set></set> is the second planet from the Sun.</template>
            </category>

            Removed tags AIML ==>
            <category><pattern>WHERE IS VENUS</pattern>
            <template>VENUS is the second planet from the Sun.</template>
            </category>
    """

    file_to_run   = os.path.join(dir_in, aiml_file)
    file_to_write = os.path.join(dir_out, aiml_file)

    def set_attributes(x_new):
        """Hard code user and bot info"""
        #x_new = x_new.replace('<get name="name"/>','friend')
        #x_new = x_new.replace('<get name="age"/>','30')
        #x_new = x_new.replace('<get name="gender"/>','male')
        #x_new = x_new.replace('<get name="location"/>','Boston')
        #x_new = x_new.replace('<get name="personality"/>','great')
        #x_new = x_new.replace('<get name="job"/>','Physicists')
        x_new = x_new.replace('<get name="name"/>','[get name="name"]')
        x_new = x_new.replace('<get name="age"/>','[get name="age"]')
        x_new = x_new.replace('<get name="gender"/>','[get name="gender"]')
        x_new = x_new.replace('<get name="location"/>','[get name="location"]')
        x_new = x_new.replace('<get name="personality"/>','[get name="personality"]')
        x_new = x_new.replace('<get name="job"/>','[get name="job"]')

        x_new = x_new.replace('<get name="it"/>','it')
        x_new = x_new.replace('<get name="memory"/>','everything')
        x_new = x_new.replace('<get name="is"/>','Physicists')
        x_new = x_new.replace('<get name="they"/>','they')
        x_new = x_new.replace('<get name="he"/>','him')
        x_new = x_new.replace('<get name="she"/>','her')
        x_new = x_new.replace('<get name="has"/>','thing')
        x_new = x_new.replace('<get name="we"/>','us')
        x_new = x_new.replace('<get name="does"/>','stuff')
        x_new = x_new.replace('<get name="like"/>','it')

        x_new = x_new.replace('<bot name="master"/>','HiBot')
        x_new = x_new.replace('<bot name="botmaster"/>','master')
        x_new = x_new.replace('<bot name="etype"/>','chatbot')
        x_new = x_new.replace('<bot name="genus"/>','chatbot')
        x_new = x_new.replace('<bot name="order"/>','chatbot')
        x_new = x_new.replace('<bot name="kingdom"/>','chatbot')
        x_new = x_new.replace('<bot name="species"/>','chatbot')
        x_new = x_new.replace('<bot name="gender"/>','chatbot')
        x_new = x_new.replace('<bot name="emotion"/>','I am electric')
        x_new = x_new.replace('<bot name="emotions"/>','I am electric')
        x_new = x_new.replace('<bot name="feelings"/>','I am electric')
        x_new = x_new.replace('<bot name="size"/>','1,000,000')
        x_new = x_new.replace('<bot name="favoritefood"/>','pizza')

        return x_new

    with open(file_to_run,'r') as f, open (file_to_write, 'w') as w:
        for x in f:
            ## Remove tags
            x_new = x.replace('</set>','').replace('<li>','').replace('</li>','').replace('<br/>','')\
                .replace('<srai>','').replace('</srai>','').replace('<star/>','')\
                .replace('<condition>','').replace('</condition>','').replace('<date>','').replace('</date>','').replace('<formal>','').replace('</formal>','')\
                .replace('<gender>','').replace('</gender>','').replace('<id>','').replace('</id>','').replace('<learn>','').replace('</learn>','')\
                .replace('<lowercase>','').replace('</lowercase>','').replace('<person>','').replace('<person/>','').replace('</person>','').replace('<person2>','').replace('</person2>','')\
                .replace('<sentence>','').replace('</sentence>','').replace('<size>','').replace('</size>','').replace('<sr>','').replace('</sr>','')\
                .replace('<system>','').replace('</system>','').replace('<that>','').replace('</that>','').replace('<thatstar>','').replace('</thatstar>','')\
                .replace('<topic>','').replace('</topic>','').replace('<topicstar>','').replace('</topicstar>','').replace('<uppercase>','').replace('</uppercase>','')\
                .replace('<version>','').replace('</version>','')
            ## Replace get tags with user info
            x_new = set_attributes(x_new)
            ## Remove all text between <think> tags
            x_new = re.sub("(<think>(.*?)</think>)", '', x_new)
            ## Replace double quotes with single
            x_new = x_new.replace('"',"'")
            ## Remove remaining set and get tags
            x_new = re.sub("(<set[^>]+>)", '', x_new)
            x_new = re.sub("(<get[^>]+>)", '', x_new)
            x_new = re.sub("(<bot[^>]+>)", '', x_new)
            x_new = re.sub("(<input[^>]+>)", '', x_new)
            ## Remove any trailing spaces
            x_new = re.sub('\s+',' ', x_new)
            w.write(x_new+'\n')


def write_JSON(aiml_file, dir_in, dir_out, tag):
    """ Convert AIML files to JSON files

        :param aiml_file: AIML file name
        :param dir_in: directory where input AIML files are location
        :param aiml_file: directory to JSON files too

        :example:
            AIML ==>
            <category><pattern>WHAT ARE THE LAWS OF THERMODYNAMICS</pattern>
            <template>I'm not a physicist, but I think this has something to do with heat, entropy, and conservation of energy, right?</template>
            </category>

            To JSON ==>
            [
                "WHAT ARE THE LAWS OF THERMODYNAMICS",
                "I'm not a physicist, but I think this has something to do with heat, entropy, and conservation of energy, right?"
            ]
    """

    json_file = aiml_file.split('.')[0]
    json_file = json_file + '.json'

    file_to_run   = os.path.join(dir_in, aiml_file)
    file_to_write = os.path.join(dir_out, json_file)

    tree = ET.parse(file_to_run)
    root = tree.getroot()

    with open (file_to_write, 'w') as w:

        ## Write the opening two lines
        w.write('{'+'\n')
        w.write('\t"' + tag + '": ['+'\n')

        ## Loop over each <category> tag and find each child node
        ## For each node, write <pattern> and <template>
        root_cnt = 0
        for child in root:
            w.write('\t\t['+'\n')

            child_cnt = 0
            for k in child:

                ## Hack to deal with <random> tags
                if len(k) > 0:
                    for j in k:
                        #k.text = str(j.text).split("[" + string.punctuation + "]+")[0]
                        #k.text = re.split("[" + string.punctuation + "]+",str(j.text))[0]
                        k.text = re.split("[\n]+",str(j.text))[0]

                ## Don't write a ',' on the last entry
                if child_cnt == len(child) - 1:
                    try:
                        w.write('\t\t\t"' + k.text + '"'+'\n')
                    except:
                        w.write('\t\t\t"' + "BLANK" + '"'+'\n')
                else:
                    try:
                        w.write('\t\t\t"' + k.text + '",'+'\n')
                    except:
                        w.write('\t\t\t"' + "BLANK" + '",'+'\n')

                child_cnt = child_cnt + 1

            ## Don't write a ',' on the last entry
            if root_cnt == len(root) - 1:
                w.write('\t\t]'+'\n')
            else:
                w.write('\t\t],'+'\n')

            root_cnt = root_cnt + 1

        w.write('\t]'+'\n')
        w.write('}'+'\n')


if __name__ == "__main__":

        ## python parse_aiml.py
        dataset_dir     = 'data/english/AIML/'
        output_no_tags  = os.path.join(dataset_dir, 'AIML_NO_TAGS/')
        output_dir      = os.path.join(dataset_dir, 'AIML_IN_JSON/')

        print("\nLoading AIML files from: %s" % dataset_dir)
        print("Writing tag free AIML files to: %s" % output_no_tags)
        print("Writing JSON version of AIML files to: %s\n" % output_dir)

        ## List of AIML files and tags
        aiml_files = [['ai.aiml','ai'],
                      ['astrology.aiml','astrology'],
                      ['atomic.aiml','atomic'],
                      #['atomic-categories0.aiml','atomic-categories0'],
                      ['biography.aiml','biography'],
                      ['computers.aiml','computers'],
                      ['drugs.aiml','drugs'],
                      ['emotion.aiml','emotion'],
                      ['geography.aiml','geography'],
                      ['knowledge.aiml','knowledge'],
                      ['misc.aiml','misc'],
                      ['music.aiml','music'],
                      ['politics.aiml','politics'],
                      ['psychology.aiml','psychology'],
                      #['pyschology.aiml','pyschology'],
                      #['religion.aiml','religion'],
                      ['sex.aiml','sex'],
                      ['sports.aiml','sports'],
                      ['science.aiml','science']
                     ]

        for aiml_file,tag in aiml_files:
            print("\tRunning file: [Tag:%s] %s" % (tag,aiml_file))

            ## Remove tag from AIML file
            remove_tags(aiml_file, dataset_dir, output_no_tags)

            ## Write to JSON
            write_JSON(aiml_file, output_no_tags, output_dir, tag = tag)

        print("\nDONE")





