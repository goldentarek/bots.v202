import unittest
import bots.botslib as botslib
import bots.botsinit as botsinit
import bots.grammar as grammar
import bots.inmessage as inmessage
import bots.outmessage as outmessage 
import utilsunit

''' plugin unitgrammar.zip '''
class TestGrammar(unittest.TestCase):

    def testgeneralgrammarerrors(self):
        self.assertRaises(botslib.GrammarError,grammar.grammarread,'flup','edifact') #not eexisting editype
        self.assertRaises(botslib.GrammarError,grammar.syntaxread,'grammars','flup','edifact') #not eexisting editype
        self.assertRaises(ImportError,grammar.grammarread,'edifact','flup')   #not existing messagetype
        self.assertRaises(ImportError,grammar.syntaxread,'grammars','edifact','flup')   #not existing messagetype
        self.assertRaises(botslib.GrammarError,grammar.grammarread,'test','test3')  #no structure
        self.assertRaises(ImportError,grammar.grammarread,'test','test4')  #No tabel - Reference to not-existing tabel
        self.assertRaises(botslib.ScriptImportError,grammar.grammarread,'test','test5')  #Error in tabel: structure is not valid python list (syntax-error)
        self.assertRaises(botslib.GrammarError,grammar.grammarread,'test','test6')  #Error in tabel: record in structure not in recorddefs
        self.assertRaises(ImportError,grammar.grammarread,'edifact','test7')   #error in syntax
        self.assertRaises(ImportError,grammar.syntaxread,'grammars','edifact','test7')   #error in syntax

    def testgramfieldedifact_and_general(self):
        tabel = grammar.grammarread('edifact','edifact')
        gramfield = tabel._checkfield
        #edifact formats to bots formats
        field =       ['S001.0001','M', 1,'A']
        fieldresult = ['S001.0001','M', 1,'A',True,0,0,'A']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        field =       ['S001.0001','M', 4,'N']
        fieldresult = ['S001.0001','M', 4,'N',True,0,0,'R']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        field =       ['S001.0001','M', 4,'AN']
        fieldresult = ['S001.0001','M', 4,'AN',True,0,0,'A']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        #min&max length
        field =       ['S001.0001','M', (2,4),'AN']
        fieldresult = ['S001.0001','M', 4,'AN',True,0,2,'A']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        field =       ['S001.0001','M', (0,4),'AN']
        fieldresult = ['S001.0001','M', 4,'AN',True,0,0,'A']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        #decimals
        field =       ['S001.0001','M', 3.2,'N']
        fieldresult = ['S001.0001','M', 3,'N',True,2,0,'R']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        field =       ['S001.0001','M', (4,4.3),'N']
        fieldresult = ['S001.0001','M', 4,'N',True,3,4,'R']
        gramfield(field,'')
        self.assertEqual(field,fieldresult),
        
        field =       ['S001.0001','M', (3.2,4.2),'N']
        fieldresult = ['S001.0001','M', 4,'N',True,2,3,'R']
        gramfield(field,'')
        self.assertEqual(field,fieldresult),
        
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #test all types of fields (I,R,N,A,D,T); tests not needed repeat for other editypes
        #check field itself
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M'],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',4],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',4,'','M', 4,'','M'],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',4,'','M', 4,''],'') 
        #check ID
        self.assertRaises(botslib.GrammarError,gramfield,['','M', 4,'A'],'') 
        self.assertRaises(botslib.GrammarError,gramfield,[None,'M', 4,'A'],'') 
        #check M/C
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','A',4,'I'],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','',4,'I'],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001',[],4,'I'],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','MC',4,'I'],'') 
        #check format
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',4,'I'],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',4,'N7'],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',4,''],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',4,5],'') 
        #check length
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M','N','N'],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',0,'N'],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',-2,'N'],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',-3.2,'N'],'')
        #length for formats without float
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',2.1,'A'],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',(2.1,3),'A'],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',(2,3.2),'A'],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',(3,2),'A'],'') 
        #length for formats with float
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',1.1,'N'],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',('A',5),'N'],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',(-1,1),'N'],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',(5,None),'N'],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',(0,1.1),'N'],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',(0,0),'N'],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',(2,1),'N'],'') 
       
    def testgramfieldx12(self):
        tabel = grammar.grammarread('x12','x12')
        gramfield = tabel._checkfield
        #x12 formats to bots formats
        field =       ['S001.0001','M', 1,'AN']
        fieldresult = ['S001.0001','M', 1,'AN',True,0,0,'A']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        field =       ['S001.0001','M', 4,'DT']
        fieldresult = ['S001.0001','M', 4,'DT',True,0,0,'D']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        field =       ['S001.0001','M', 4,'TM']
        fieldresult = ['S001.0001','M', 4,'TM',True,0,0,'T']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        field =       ['S001.0001','M', 4,'B']
        fieldresult = ['S001.0001','M', 4,'B',True,0,0,'A']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        field =       ['S001.0001','M', 4,'ID']
        fieldresult = ['S001.0001','M', 4,'ID',True,0,0,'A']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        field =       ['S001.0001','M', 4,'R']
        fieldresult = ['S001.0001','M', 4,'R',True,0,0,'R']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        field =       ['S001.0001','M', 4,'N']
        fieldresult = ['S001.0001','M', 4,'N',True,0,0,'I']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        field =       ['S001.0001','M', 4,'N0']
        fieldresult = ['S001.0001','M', 4,'N0',True,0,0,'I']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        field =       ['S001.0001','M', 4,'N3']
        fieldresult = ['S001.0001','M', 4,'N3',True,3,0,'I']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        field =       ['S001.0001','M', 4,'N9']
        fieldresult = ['S001.0001','M', 4,'N9',True,9,0,'I']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        #decimals
        field =       ['S001.0001','M', 3,'R']
        fieldresult = ['S001.0001','M', 3,'R',True,0,0,'R']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        field =       ['S001.0001','M',4.3,'R']
        fieldresult = ['S001.0001','M', 4,'R',True,3,0,'R']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',4,'D'],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',4.3,'I'],'') 
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',4.3,'NO'],'') 

        
    def testgramfieldfixed(self):
        tabel = grammar.grammarread('fixed','invoicfixed')
        gramfield = tabel._checkfield
        #fixed formats to bots formats
        field =       ['S001.0001','M', 1,'A']
        fieldresult = ['S001.0001','M', 1,'A',True,0,1,'A']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        field =       ['S001.0001','M', 4,'D']
        fieldresult = ['S001.0001','M', 4,'D',True,0,4,'D']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        field =       ['S001.0001','M', 4,'T']
        fieldresult = ['S001.0001','M', 4,'T',True,0,4,'T']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        field =       ['S001.0001','M', 4,'R']
        fieldresult = ['S001.0001','M', 4,'R',True,0,4,'R']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        field =       ['S001.0001','M', 4.3,'N']
        fieldresult = ['S001.0001','M', 4,'N',True,3,4,'N']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        field =       ['S001.0001','M', 4.3,'I']
        fieldresult = ['S001.0001','M', 4,'I',True,3,4,'I']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        field =       ['S001.0001','M',4.3,'R']
        fieldresult = ['S001.0001','M', 4,'R',True,3,4,'R']
        gramfield(field,'')
        self.assertEqual(field,fieldresult)
        
        self.assertRaises(botslib.GrammarError,gramfield,['S001.0001','M',4,'B'],'') 



if __name__ == '__main__':
    botsinit.generalinit('config')
    #~ botslib.initbotscharsets()
    botsinit.initenginelogging()
    unittest.main()
