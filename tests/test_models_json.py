"""Tests for JSON-based model filtering."""

import json

from pathlib import Path

import pytest

from ecologits.model_repository import Architecture, ArchitectureTypes, Deployment, Model, Providers

from src.repositories import models as models_repo
from src.repositories.model_config import load_main_models
from src.repositories.models import load_models


def _make_model(name: str, provider: Providers = Providers.openai) -> Model:
    return Model(
        provider=provider,
        name=name,
        architecture=Architecture(type=ArchitectureTypes.DENSE, parameters=7.0),
        warnings=[],
        sources=[],
        deployment=Deployment(tps=10.0, ttft=0.1),
    )


class TestJSONModelFiltering:
    """Test cases for JSON-based model filtering."""

    def test_load_main_models_from_json(self) -> None:
        """Should load main models from models_recent.json file."""
        main_models = load_main_models()

        assert isinstance(main_models, list)
        assert len(main_models) > 0
        assert all(isinstance(name, str) and name for name in main_models)
        assert len(main_models) == len(set(main_models)), "Model names should be unique"

    def test_json_file_exists(self) -> None:
        """Should have models_recent.json file."""
        json_path = Path(__file__).resolve().parent.parent / "src" / "config" / "models_recent.json"
        assert json_path.exists(), "models_recent.json file should exist"

    def test_json_file_structure(self) -> None:
        """Should have valid JSON structure."""
        json_path = Path(__file__).resolve().parent.parent / "src" / "config" / "models_recent.json"

        with open(json_path) as f:
            data = json.load(f)

        assert "models" in data
        assert isinstance(data["models"], list)
        assert len(data["models"]) > 0

        for model in data["models"]:
            assert "provider" in model
            assert "name" in model
            assert isinstance(model["provider"], str)
            assert isinstance(model["name"], str)

    def test_model_filtering_works(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Should correctly filter models based on the main models list."""
        repo_models = [
            _make_model("model-a"),
            _make_model("model-b"),
            _make_model("model-c", Providers.anthropic),
        ]
        monkeypatch.setattr(models_repo.model_repository, "list_models", lambda: repo_models)
        monkeypatch.setattr(models_repo, "load_main_models", lambda: ["model-c", "model-a"])

        df_filtered = load_models(filter_main=True)
        df_all = load_models(filter_main=False)

        assert len(df_filtered) < len(df_all)
        assert df_filtered["name"].tolist() == ["model-c", "model-a"]
        assert sorted(df_all["name"].tolist()) == ["model-a", "model-b", "model-c"]

        main_models = ["model-a", "model-c"]
        for model_name in df_filtered["name"]:
            assert model_name in main_models

    def test_load_errors_propagate(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Missing or corrupt JSON must fail loudly, not fall back."""
        import src.repositories.model_config as model_config

        def _raise_json_error(*_args, **_kwargs) -> None:
            raise json.JSONDecodeError("test", "", 0)

        monkeypatch.setattr(model_config.json, "load", _raise_json_error)

        with pytest.raises(json.JSONDecodeError):
            load_main_models()

    def test_every_listed_model_exists_in_repository(self) -> None:
        """Every name in models_recent.json must exist in ecologits repository."""
        from ecologits.model_repository import models as model_repository

        available = {m.name for m in model_repository.list_models()}
        for name in load_main_models():
            assert name in available, (
                f"{name!r} listed in models_recent.json but missing from ecologits repository"
            )


class TestModelFilteringIntegration:
    """Integration-style tests for model filtering using synthetic data."""

    def test_filtered_ui_uses_main_models(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Filtered UI modes should only expose models from the main list."""
        repo_models = [
            _make_model("openai-main", Providers.openai),
            _make_model("openai-extra", Providers.openai),
            _make_model("anthropic-main", Providers.anthropic),
        ]
        monkeypatch.setattr(models_repo.model_repository, "list_models", lambda: repo_models)
        monkeypatch.setattr(
            models_repo, "load_main_models", lambda: ["openai-main", "anthropic-main"]
        )

        df_filtered = load_models(filter_main=True)

        assert sorted(df_filtered["name"].tolist()) == ["anthropic-main", "openai-main"]
        providers = df_filtered["provider_clean"].unique().tolist()
        assert "OpenAI" in providers
        assert "Anthropic" in providers

    def test_expert_mode_uses_all_models(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Expert mode should have access to the full unfiltered model list."""
        repo_models = [
            _make_model("model-1", Providers.openai),
            _make_model("model-2", Providers.anthropic),
        ]
        monkeypatch.setattr(models_repo.model_repository, "list_models", lambda: repo_models)
        monkeypatch.setattr(models_repo, "load_main_models", lambda: ["model-1"])

        df_all = load_models(filter_main=False)
        df_filtered = load_models(filter_main=True)

        assert len(df_all) > len(df_filtered)
        assert set(df_filtered["name"]).issubset(set(df_all["name"]))
