from pydoc import visiblename
from vocabulary_creator import VocabularyCreator
import unittest
from unittest.mock import patch

class TestVocabularyCreator(unittest.TestCase):
    def setUp(self):
        self.mails = { "dataset": [
        {
        "mail": {
        "Subject": " you ve received a greeting from a family member !",
        "From": "SA_and_HP@paris.com",
        "Date": "2005-07-18",
        "Body":"d >\nyou have just received a virtual\npostcard from a family member !\n.\nyou can pick up your postcard at\nthe following web address :\n.\n.\nif you can t click on the web address\nabove you can also\nvisit 1001 postcards at http : www . postcards . org postcards \nand enter your pickup code which is : a 91 - valets - cloud - mad\n.\n( your postcard will be available\nfor 60 days . )\n.\noh - - and if you d like to reply\nwith a postcard \nyou can do so by visiting this web address :\nhttp : www 2 . postcards . org \n( or you can simply click the reply to this postcard\nbutton beneath your postcard ! )\n.\nwe hope you enjoy your postcard \nand if you do \nplease take a moment to send a few yourself !\n.\nregards \n1001 postcards\nhttp : www . postcards . org postcards \n",
        "Spam": "true",
        "File": "enronds//enron2/spam/4995.2005-07-18.SA_and_HP.spam.txt"
        }
        }, 
        {
        "mail": {
        "Subject": " re : eol phase 2",
        "From": "kaminski@paris.com",
        "Date": "2000-07-05",
        "Body":"deal all \ni have written the option pricing formula for european ( euro ) american\n( amer ) and asian ( agc ) options .\ni have also cited the references for each option . the function names in ( )\nare the option models in the\nenron exotica options library . you do not have to have outside programmer\nto duplicate our work since we have\nconstructed and tested these models .\nif you have any questions please let me know .\nzimin\nvince j kaminski\n06 30 2000 02 : 31 pm\nto : michael danielson hou ect @ ect\ncc : stinson gibner hou ect @ ect zimin lu hou ect @ ect vince j\nkaminski hou ect @ ect\nsubject : re : eol phase 2\nmichael \nplease contact zimin lu .\nvince kaminski\nmichael danielson\n06 30 2000 01 : 10 pm\nto : vince j kaminski hou ect @ ect mike a roberts hou ect @ ect\ncc : angela connelly lon ect @ ect savita puthigai na enron @ enron\nsubject : eol phase 2\nthanks for your help on content for eol phase 2 .\nan additional piece of content that we are trying to include in our scope is\nan options calculator . this would be an interactive tool to teach less\nsophisticated counterparties about options . we would like to collaborate\nwith someone in research to refine our approach ( and make sure we re using\nthe right formulas ) . who should we contact in research for this ?\nattached is a mock - up of what we have in mind . . .\n- calculator prototype . pp\n",
        "Spam": "false",
        "File": "enronds//enron2/ham/1683.2000-07-05.kaminski.ham.txt"
        }
        }
        ]}  # données pour mocker "return_value" du "load_dict"
        self.clean_subject_spam = [" you ve received a greeting from a family member !"]  # données pour mocker "return_value" du "clean_text"
        self.clean_body_spam = ["d >\nyou have just received a virtual\npostcard from a family member !\n.\nyou can pick up your postcard at\nthe following web address :\n.\n.\nif you can t click on the web address\nabove you can also\nvisit 1001 postcards at http : www . postcards . org postcards \nand enter your pickup code which is : a 91 - valets - cloud - mad\n.\n( your postcard will be available\nfor 60 days . )\n.\noh - - and if you d like to reply\nwith a postcard \nyou can do so by visiting this web address :\nhttp : www 2 . postcards . org \n( or you can simply click the reply to this postcard\nbutton beneath your postcard ! )\n.\nwe hope you enjoy your postcard \nand if you do \nplease take a moment to send a few yourself !\n.\nregards \n1001 postcards\nhttp : www . postcards . org postcards \n"]  # données pour mocker "return_value" du "clean_text"
        self.clean_subject_ham = [" celebration"]  # données pour mocker "return_value" du "clean_text"
        self.clean_body_ham = ["i am so excited for my boss mike robert s .\ni was wondering : can we do something special\nfor him celebrating his promotion ?\nkevin moor\n"]  # données pour mocker "return_value" du "clean_text"
        self.vocab_expected = {
            "p_sub_spam": {
                " you ve": 0.5,
                "greeting": 0.5,
                "family": 0.5
            },
            "p_body_spam": {
                "celebration": 0.3333333333333333,
                "www 2 .": 0.3333333333333333,
                ". org": 0.3333333333333333
            },
            "p_sub_ham": {
                "re": 0.3333333333333333,
                "eol": 0.3333333333333333,
                "phase": 0.3333333333333333
            },
            "p_body_ham": {
                "european": 0.2,
                "american": 0.2,
                "eol": 0.2,
                "phase": 0.2
            }
        }  # vocabulaire avec les valeurs de la probabilité calculées correctement

    def tearDown(self):
        pass

    @patch("vocabulary_creator.VocabularyCreator.load_dict")
    @patch("vocabulary_creator.VocabularyCreator.clean_text")
    @patch("vocabulary_creator.VocabularyCreator.write_data_to_vocab_file")
    def test_create_vocab_spam_Returns_vocabulary_with_correct_values(
        self, mock_write_data_to_vocab_file, mock_clean_text, mock_load_dict
    ):
        """Description: Tester qu'un vocabulaire avec les probabilités calculées
        correctement va être retourné. Il faut mocker les fonctions "load dict"
         (utiliser self.mails comme une simulation de valeur de retour),"clean text"
         (cette fonction va être appelée quelques fois, pour chaque appel on
         va simuler une valeur de retour differente, pour cela il faut utiliser
         side_effect (voir l'exemple dans l'énonce)) et
         "write_data_to_vocab_file" qui va simuler "return True" au lieu
         d'écrire au fichier "vocabulary.json".
         if faut utiliser self.assertEqual(appel_a_create_vocab(), self.vocab_expected)
        """
        values = {'a': self.clean_subject_spam, 'b': self.clean_body_spam, 'c': self.clean_subject_ham, 'd': self.clean_body_ham}
        def side_effect(arg):
            return values[arg]
        mock_load_dict.return_value = self.mails
        mock_clean_text.return_value = side_effect
        mock_write_data_to_vocab_file.return_value = True
        vocabularyCreator = VocabularyCreator()
        vocabularyCreator.create_vocab()
        self.assertEqual(vocabularyCreator.voc_data, self.vocab_expected)
        pass
    
    ###########################################
    #               CUSTOM TEST               #
    ###########################################