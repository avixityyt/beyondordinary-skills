import datetime
import json
import os
import pathlib
import tempfile
import unittest
from unittest.mock import patch
import sys
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from review_submission import allowed_path,check_files,signals,duplicates,main

class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=pathlib.Path(self.temp.name)
        self.now=datetime.datetime(2026,10,6,tzinfo=datetime.timezone.utc)
    def tearDown(self):self.temp.cleanup()
    def test_contributors_cannot_modify_tooling_workflows_or_rename_outside_skill_paths(self):
        for name in ['.github/workflows/validate.yml','tools/validate.py','README.md','skills/example/../escape','previews/example.png','skills/example/.git/config']:
            self.assertFalse(allowed_path(name))
            with self.assertRaises(ValueError):check_files(self.root,[{'filename':name}],99)
        with self.assertRaises(ValueError):check_files(self.root,[{'filename':'skills/example/SKILL.md','previous_filename':'tools/validate.py'}],99)
        check_files(self.root,[{'filename':'tools/validate.py'}],74422918)
    def test_changed_file_count_and_sizes_are_bounded(self):
        with self.assertRaises(ValueError):check_files(self.root,[{'filename':'skills/example/file.txt'}]*61,99)
        folder=self.root/'skills/example';folder.mkdir(parents=True)
        (folder/'large.txt').write_bytes(b'x'*2_000_001)
        with self.assertRaises(ValueError):check_files(self.root,[{'filename':'skills/example/large.txt'}],99)
        for i in range(3):(folder/f'{i}.txt').write_bytes(b'x'*1_800_000)
        with self.assertRaises(ValueError):check_files(self.root,[{'filename':f'skills/example/{i}.txt'} for i in range(3)],99)
    def test_symlinks_are_rejected(self):
        folder=self.root/'skills/example';folder.mkdir(parents=True);(folder/'file.txt').symlink_to(self.root/'elsewhere')
        with self.assertRaises(ValueError):check_files(self.root,[{'filename':'skills/example/file.txt'}],99)
    def test_new_accounts_bots_and_submission_bursts_are_review_signals_only(self):
        pulls=[{'user':{'id':99},'created_at':'2026-10-05T23:00:00Z'} for _ in range(4)]
        self.assertEqual(len(signals({'type':'Bot','created_at':'2026-10-05T00:00:00Z'},pulls,99,self.now)),3)
        self.assertEqual(signals({'type':'User','created_at':'2020-01-01T00:00:00Z'},pulls,100,self.now),[])
    def test_duplicate_bodies_ignore_frontmatter_names_and_whitespace_but_allow_own_updates(self):
        base=self.root/'base';root=self.root/'submission'
        for directory,slug,body in [(base,'original','Make the output.'),(root,'copy','Make  the\noutput.'),(root,'original','Make the output.')]:
            folder=directory/'skills'/slug;folder.mkdir(parents=True)
            (folder/'SKILL.md').write_text(f'---\nname: {slug}\ndescription: An example.\n---\n{body}')
        self.assertTrue(duplicates(root,base,[{'filename':'skills/copy/SKILL.md','status':'added'}]))
        self.assertEqual(duplicates(root,base,[{'filename':'skills/original/SKILL.md','status':'modified'}]),[])
    def test_main_writes_review_summary_without_write_api_calls(self):
        root=self.root/'submission';base=self.root/'base';root.mkdir();base.mkdir()
        event={'pull_request':{'number':7,'user':{'id':99,'login':'example'},'base':{'repo':{'full_name':'avixityyt/beyondordinary-skills'}}}}
        path=self.root/'event.json';path.write_text(json.dumps(event));summary=self.root/'summary.md'
        with patch.dict(os.environ,{'GITHUB_EVENT_PATH':str(path),'GITHUB_STEP_SUMMARY':str(summary)}),patch.object(sys,'argv',['review',str(root),str(base)]),patch('review_submission.api',side_effect=[[],{'id':99,'type':'User','created_at':'2020-01-01T00:00:00Z'},[]]) as api:
            main()
        self.assertIn('do not automatically reject',summary.read_text())
        self.assertEqual(api.call_count,3)

if __name__=='__main__':unittest.main()
