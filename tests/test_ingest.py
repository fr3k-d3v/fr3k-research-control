import importlib.util,pathlib,tempfile,unittest
spec=importlib.util.spec_from_file_location('ingest',pathlib.Path(__file__).resolve().parents[1]/'scripts/ingest.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestIngest(unittest.TestCase):
 def test_dedup_metadata_and_secrets(self):
  with tempfile.TemporaryDirectory() as d:
   p=pathlib.Path(d);(p/'a.md').write_text('hello');(p/'token.txt').write_text('sensitive');(p/'x.gguf').write_bytes(b'abc')
   r=m.collect([p]);self.assertEqual(len(r),1);self.assertEqual(r[0]['relative_path'],'a.md');self.assertEqual(len(r[0]['sha256']),64)
if __name__=='__main__':unittest.main()
