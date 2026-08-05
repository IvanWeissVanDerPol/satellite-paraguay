"""Tests for src/utils/deploy_templates.py."""
import pytest
from pathlib import Path


class TestDeployTemplates:
    """Tests for deploy_templates module."""

    def test_build_docker_compose_returns_string(self):
        from src.utils.deploy_templates import build_docker_compose
        result = build_docker_compose()
        assert isinstance(result, str)
        assert "services:" in result
        assert "postgres" in result
        assert "redis" in result
        assert "fastapi" in result
        assert "streamlit" in result

    def test_build_dockerfile_returns_string(self):
        from src.utils.deploy_templates import build_dockerfile
        result = build_dockerfile()
        assert isinstance(result, str)
        assert "FROM python" in result
        assert "WORKDIR /app" in result
        assert "EXPOSE" in result

    def test_build_github_actions_returns_string(self):
        from src.utils.deploy_templates import build_github_actions
        result = build_github_actions()
        assert isinstance(result, str)
        assert "name: CI/CD" in result
        assert "jobs:" in result
        assert "test:" in result
        assert "deploy:" in result

    def test_build_prometheus_config_returns_string(self):
        from src.utils.deploy_templates import build_prometheus_config
        result = build_prometheus_config()
        assert isinstance(result, str)
        assert "scrape_interval" in result
        assert "fastapi" in result

    def test_write_docker_compose(self, tmp_path):
        from src.utils.deploy_templates import write_docker_compose, build_docker_compose
        content = build_docker_compose()
        out = tmp_path / "docker-compose.yml"
        write_docker_compose(content, out)
        assert out.exists()
        assert "services:" in out.read_text()

    def test_write_dockerfile(self, tmp_path):
        from src.utils.deploy_templates import write_dockerfile, build_dockerfile
        content = build_dockerfile()
        out = tmp_path / "Dockerfile"
        write_dockerfile(content, out)
        assert out.exists()

    def test_write_github_actions_creates_parent(self, tmp_path):
        from src.utils.deploy_templates import write_github_actions, build_github_actions
        content = build_github_actions()
        out = tmp_path / ".github" / "workflows" / "cicd.yml"
        write_github_actions(content, out)
        assert out.exists()

    def test_write_prometheus_config_creates_parent(self, tmp_path):
        from src.utils.deploy_templates import write_prometheus_config, build_prometheus_config
        content = build_prometheus_config()
        out = tmp_path / "monitoring" / "prometheus.yml"
        write_prometheus_config(content, out)
        assert out.exists()

    def test_all_templates_have_content(self):
        """All template builders produce non-empty content."""
        from src.utils.deploy_templates import (
            build_docker_compose,
            build_dockerfile,
            build_github_actions,
            build_prometheus_config,
        )
        for builder in [build_docker_compose, build_dockerfile, build_github_actions, build_prometheus_config]:
            content = builder()
            assert len(content) > 50, f"{builder.__name__} produced too little content"