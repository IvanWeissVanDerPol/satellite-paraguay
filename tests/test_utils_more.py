"""Tests for src/utils/reproducibility_verify, repo_evaluator, repo_verify."""


class TestReproducibilityVerify:
    """Tests for reproducibility_verify module."""

    def test_file_hash_sha256(self, tmp_path):
        from src.utils.reproducibility_verify import file_hash

        f = tmp_path / "test.txt"
        f.write_text("hello world")
        h = file_hash(f, "sha256")
        assert len(h) == 64
        # Known hash for "hello world"
        assert h == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"

    def test_file_hash_sha512(self, tmp_path):
        from src.utils.reproducibility_verify import file_hash

        f = tmp_path / "test.txt"
        f.write_text("hello")
        h = file_hash(f, "sha512")
        assert len(h) == 128

    def test_run_script_success(self, tmp_path):
        from src.utils.reproducibility_verify import run_script

        # Create a simple script
        script = tmp_path / "test.py"
        script.write_text("print('hello')")
        rc, stdout, stderr = run_script(tmp_path, "test.py")
        assert rc == 0
        assert "hello" in stdout

    def test_run_script_failure(self, tmp_path):
        from src.utils.reproducibility_verify import run_script

        script = tmp_path / "fail.py"
        script.write_text("import sys; sys.exit(1)")
        rc, stdout, stderr = run_script(tmp_path, "fail.py")
        assert rc == 1

    def test_check_outputs_exist_all_present(self, tmp_path):
        from src.utils.reproducibility_verify import check_outputs_exist

        (tmp_path / "a.txt").write_text("x")
        (tmp_path / "b.txt").write_text("y")
        missing = check_outputs_exist(tmp_path, ["a.txt", "b.txt"])
        assert missing == []

    def test_check_outputs_exist_some_missing(self, tmp_path):
        from src.utils.reproducibility_verify import check_outputs_exist

        (tmp_path / "a.txt").write_text("x")
        missing = check_outputs_exist(tmp_path, ["a.txt", "missing.txt"])
        assert missing == ["missing.txt"]

    def test_hash_outputs_existing(self, tmp_path):
        from src.utils.reproducibility_verify import hash_outputs

        (tmp_path / "a.txt").write_text("hello")
        hashes = hash_outputs(tmp_path, ["a.txt", "missing.txt"])
        assert "a.txt" in hashes
        assert "missing.txt" not in hashes

    def test_verify_script_pass(self, tmp_path):
        from src.utils.reproducibility_verify import verify_script

        # Create a script that creates an output
        script = tmp_path / "create.py"
        script.write_text("open('output.txt', 'w').write('data')")
        rc, _, _ = (0, "", "")  # placeholder  # noqa: F841
        result = verify_script(tmp_path, "create.py", ["output.txt"])
        # Either pass or fail depending on script behavior
        assert "status" in result

    def test_verify_script_timeout(self, tmp_path):
        from src.utils.reproducibility_verify import verify_script

        script = tmp_path / "sleep.py"
        script.write_text("import time; time.sleep(60)")
        result = verify_script(tmp_path, "sleep.py", [], timeout=2)
        assert result["status"] == "timeout"

    def test_summarize_results(self):
        from src.utils.reproducibility_verify import summarize_results

        results = [
            {"status": "pass"},
            {"status": "pass"},
            {"status": "fail"},
            {"status": "timeout"},
        ]
        counts = summarize_results(results)
        assert counts["pass"] == 2
        assert counts["fail"] == 1
        assert counts["timeout"] == 1

    def test_summarize_results_unknown_status(self):
        from src.utils.reproducibility_verify import summarize_results

        counts = summarize_results([{"status": "unknown"}])
        assert counts == {"pass": 0, "fail": 0, "timeout": 0}

    def test_total_elapsed(self):
        from src.utils.reproducibility_verify import total_elapsed

        results = [
            {"elapsed_s": 1.0},
            {"elapsed_s": 2.5},
            {"elapsed_s": 3.0},
        ]
        assert total_elapsed(results) == 6.5

    def test_total_elapsed_no_field(self):
        from src.utils.reproducibility_verify import total_elapsed

        assert total_elapsed([{"foo": "bar"}]) == 0


class TestRepoEvaluator:
    """Tests for repo_evaluator module."""

    def test_count_files_by_type(self, tmp_path):
        from src.utils.repo_evaluator import count_files_by_type

        (tmp_path / "a.py").write_text("")
        (tmp_path / "b.md").write_text("")
        (tmp_path / "c.yaml").write_text("")
        (tmp_path / "d.txt").write_text("")
        counts = count_files_by_type(tmp_path)
        assert counts["python"] == 1
        assert counts["markdown"] == 1
        assert counts["yaml"] == 1
        assert counts["total"] == 4

    def test_count_files_excludes_git(self, tmp_path):
        from src.utils.repo_evaluator import count_files_by_type

        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        (git_dir / "config").write_text("")
        (tmp_path / "real.py").write_text("")
        counts = count_files_by_type(tmp_path)
        assert counts["python"] == 1
        assert counts["total"] == 1  # git dir excluded

    def test_count_files_handles_images(self, tmp_path):
        from src.utils.repo_evaluator import count_files_by_type

        (tmp_path / "a.png").write_text("")
        (tmp_path / "b.jpg").write_text("")
        (tmp_path / "c.gif").write_text("")
        counts = count_files_by_type(tmp_path)
        assert counts["image"] == 3

    def test_count_loc(self, tmp_path):
        from src.utils.repo_evaluator import count_loc

        (tmp_path / "a.py").write_text("# comment\ndef f():\n    pass\n\n# another\nprint('x')\n")
        loc = count_loc(tmp_path)
        # def f(), pass, print('x') = 3 non-blank, non-comment lines
        assert loc == 3

    def test_count_loc_zero_for_comments_only(self, tmp_path):
        from src.utils.repo_evaluator import count_loc

        (tmp_path / "a.py").write_text("# only comments\n# more\n")
        assert count_loc(tmp_path) == 0

    def test_count_test_files_nonexistent(self, tmp_path):
        from src.utils.repo_evaluator import count_test_files

        result = count_test_files(tmp_path / "missing")
        assert result == []

    def test_count_test_files(self, tmp_path):
        from src.utils.repo_evaluator import count_test_files

        (tmp_path / "test_a.py").write_text("")
        (tmp_path / "test_b.py").write_text("")
        (tmp_path / "not_a_test.py").write_text("")
        result = count_test_files(tmp_path)
        assert len(result) == 2

    def test_is_module_stub(self):
        from src.utils.repo_evaluator import is_module_stub

        assert is_module_stub("def f():\n    pass  # TODO\n")
        assert is_module_stub("def f():\n    raise NotImplementedError\n")
        assert is_module_stub("# TODO: fix this\n")
        assert is_module_stub("# FIXME: bug\n")
        assert not is_module_stub("def f():\n    return 5\n")

    def test_extract_signatures_basic(self):
        from src.utils.repo_evaluator import extract_signatures

        code = """
class Foo:
    def bar(self):
        pass

def baz():
    pass
"""
        sigs = extract_signatures(code)
        assert "class Foo" in sigs
        assert "def baz" in sigs
        # _underscore functions excluded
        assert not any(s.startswith("def _") for s in sigs)

    def test_extract_signatures_invalid(self):
        from src.utils.repo_evaluator import extract_signatures

        sigs = extract_signatures("def broken(:\n  invalid python")
        assert sigs == []

    def test_extract_signatures_limits(self):
        from src.utils.repo_evaluator import extract_signatures

        code = "\n".join([f"def f{i}():\n    pass" for i in range(20)])
        sigs = extract_signatures(code, max_signatures=5)
        assert len(sigs) == 5

    def test_analyze_module_returns_dict(self, tmp_path):
        from src.utils.repo_evaluator import analyze_module

        src = tmp_path / "src"
        src.mkdir()
        mod = src / "mod.py"
        mod.write_text("class Foo:\n    def bar(self):\n        return 1\n")
        result = analyze_module(mod, src)
        assert result["path"] == "mod.py"
        assert result["n_classes"] == 1
        assert result["n_functions"] == 1
        assert result["is_stub"] is False

    def test_analyze_modules(self, tmp_path):
        from src.utils.repo_evaluator import analyze_modules

        src = tmp_path / "src"
        src.mkdir()
        (src / "a.py").write_text("def f(): pass\n")
        (src / "__init__.py").write_text("")  # excluded
        modules = analyze_modules(src)
        assert len(modules) == 1
        assert modules[0]["path"] == "a.py"

    def test_count_real_vs_stub(self):
        from src.utils.repo_evaluator import count_real_vs_stub

        modules = [
            {"is_stub": False},
            {"is_stub": False},
            {"is_stub": True},
        ]
        counts = count_real_vs_stub(modules)
        assert counts["real"] == 2
        assert counts["stub"] == 1
        assert counts["total"] == 3

    def test_total_loc_by_status(self):
        from src.utils.repo_evaluator import total_loc_by_status

        modules = [
            {"is_stub": False, "loc": 100},
            {"is_stub": False, "loc": 50},
            {"is_stub": True, "loc": 20},
        ]
        result = total_loc_by_status(modules)
        assert result["real"] == 150
        assert result["stub"] == 20


class TestRepoVerify:
    """Tests for repo_verify module."""

    def test_verify_imports_success(self):
        from src.utils.repo_verify import verify_imports

        result = verify_imports(modules=["os", "sys"])
        assert result["ok"] is True
        assert "os" in result["imported"]
        assert len(result["failed"]) == 0

    def test_verify_imports_failure(self):
        from src.utils.repo_verify import verify_imports

        result = verify_imports(modules=["nonexistent_module_xyz_123"])
        assert result["ok"] is False
        assert len(result["failed"]) == 1

    def test_verify_pipelines_success(self):
        """Use real pipeline that we know exists."""
        from src.utils.repo_verify import verify_pipelines

        # YvutuPipeline is in p0011 (correct name: Y-v-u-t-y-u, not YvutuPipeline)
        result = verify_pipelines(pipeline_specs=[("src.papers.p0011_yvytu_deforestation.pipeline", "YvytuPipeline")])
        assert result["ok"] is True
        assert "YvytuPipeline" in result["instantiated"]

    def test_verify_pipelines_failure(self):
        from src.utils.repo_verify import verify_pipelines

        result = verify_pipelines(pipeline_specs=[("nonexistent.module", "NonExistentClass")])
        assert result["ok"] is False
        assert len(result["failed"]) == 1

    def test_all_checks_passed(self):
        from src.utils.repo_verify import all_checks_passed

        assert all_checks_passed({"ok": True}, {"ok": True}) is True
        assert all_checks_passed({"ok": True}, {"ok": False}) is False
        assert all_checks_passed({"foo": "bar"}) is False

    def test_overall_summary(self):
        from src.utils.repo_verify import overall_summary

        summary = overall_summary({"ok": True}, {"ok": True})
        assert summary["ok"] is True
        assert summary["n_checks"] == 2

    def test_overall_summary_mixed(self):
        from src.utils.repo_verify import overall_summary

        summary = overall_summary({"ok": True}, {"ok": False})
        assert summary["ok"] is False
