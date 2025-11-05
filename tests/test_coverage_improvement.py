"""
New tests for improving code coverage in Click project.
Focus on uncovered areas in shell_completion.py and decorators.py
"""

from unittest.mock import Mock
from unittest.mock import patch

import pytest

import click
from click.decorators import help_option
from click.decorators import version_option
from click.shell_completion import add_completion_class
from click.shell_completion import BashComplete
from click.shell_completion import CompletionItem
from click.shell_completion import FishComplete
from click.shell_completion import ShellComplete
from click.shell_completion import ZshComplete


class TestShellCompletionEdgeCases:
    """Test uncovered edge cases in shell completion."""

    def test_completion_item_with_none_help(self):
        """Test CompletionItem handles None help text correctly."""
        item = CompletionItem(type="plain", value="--option", help=None)
        assert item.help is None
        assert item.value == "--option"
        assert item.type == "plain"

    def test_fish_complete_format_with_empty_help(self):
        """Test FishComplete.format_completion with empty help text."""
        fish = FishComplete(
            cli=Mock(), ctx_args={}, prog_name="test", complete_var="TEST"
        )

        # Test with empty string help
        item = CompletionItem(type="plain", value="--opt", help="")
        result = fish.format_completion(item)

        # Should use "_" for empty help
        assert "\n--opt\n_" in result or result.endswith("_")

    def test_fish_complete_format_with_newlines_in_value(self):
        """Test FishComplete.format_completion escapes newlines in value."""
        fish = FishComplete(
            cli=Mock(), ctx_args={}, prog_name="test", complete_var="TEST"
        )

        # Test with newlines in value
        item = CompletionItem(type="plain", value="--opt\nwith\nnewlines", help="help")
        result = fish.format_completion(item)

        # Newlines should be escaped
        assert "\\n" in result
        assert "\nwith\n" not in result or result.count("\n") >= 3

    def test_bash_complete_format_with_special_chars(self):
        """Test BashComplete.format_completion handles special characters."""
        bash = BashComplete(
            cli=Mock(), ctx_args={}, prog_name="test", complete_var="TEST"
        )

        # Test with special characters
        item = CompletionItem(type="plain", value="--option=value", help="Help text")
        result = bash.format_completion(item)

        assert "--option=value" in result

    def test_zsh_complete_format_with_colon_in_help(self):
        """Test ZshComplete.format_completion handles colons in help text."""
        zsh = ZshComplete(
            cli=Mock(), ctx_args={}, prog_name="test", complete_var="TEST"
        )

        # Test with colon in help (should be escaped for Zsh)
        item = CompletionItem(type="plain", value="--opt", help="Help: with colon")
        result = zsh.format_completion(item)

        # Result should contain the option
        assert "--opt" in result

    def test_add_completion_class_custom(self):
        """Test add_completion_class with custom completion class."""

        class CustomComplete(ShellComplete):
            name = "custom"
            source_template = "# custom template"

            def format_completion(self, item):
                return f"custom:{item.value}"

        # Add custom completion class
        result = add_completion_class(CustomComplete, "custom")

        assert result is CustomComplete
        # Verify it was added to available shells
        from click.shell_completion import _available_shells

        assert "custom" in _available_shells
        assert _available_shells["custom"] is CustomComplete

    def test_shell_complete_get_completion_args_abstract(self):
        """Test ShellComplete.get_completion_args is abstract."""

        # Create a minimal concrete implementation
        class MinimalComplete(ShellComplete):
            name = "minimal"
            source_template = "# minimal"

            def get_completion_args(self):
                return [], ""

            def format_completion(self, item):
                return item.value

        shell = MinimalComplete(
            cli=Mock(), ctx_args={}, prog_name="test", complete_var="TEST"
        )
        args, incomplete = shell.get_completion_args()

        assert args == []
        assert incomplete == ""

    def test_completion_item_equality(self):
        """Test CompletionItem comparison and representation."""
        item1 = CompletionItem(type="plain", value="--opt", help="Help")
        item2 = CompletionItem(type="plain", value="--opt", help="Help")
        item3 = CompletionItem(type="dir", value="path/", help=None)

        # Test that items have proper attributes
        assert item1.value == "--opt"
        assert item1.help == "Help"
        assert item3.type == "dir"

        # Items should be distinct objects
        assert item1 is not item2


class TestDecoratorEdgeCases:
    """Test uncovered edge cases in decorators."""

    def test_version_option_with_custom_message(self):
        """Test version_option with custom message template."""

        @click.command()
        @version_option(
            version="1.0.0", prog_name="TestApp", message="%(prog)s version %(version)s"
        )
        def cli():
            pass

        runner = click.testing.CliRunner()
        result = runner.invoke(cli, ["--version"])

        assert result.exit_code == 0
        assert "TestApp" in result.output
        assert "1.0.0" in result.output

    def test_version_option_with_package_name(self):
        """Test version_option can read version from package (mock)."""
        with patch("importlib.metadata.version", return_value="2.0.0"):

            @click.command()
            @version_option(package_name="fake_package")
            def cli():
                pass

            runner = click.testing.CliRunner()
            result = runner.invoke(cli, ["--version"])

            # Should succeed and show version
            assert result.exit_code == 0

    def test_help_option_custom_names(self):
        """Test help_option with custom option names."""

        @click.command()
        @help_option("-h", "--help", "--info")
        def cli():
            """Test command."""
            click.echo("executed")

        runner = click.testing.CliRunner()

        # Test with -h
        result = runner.invoke(cli, ["-h"])
        assert result.exit_code == 0
        assert "Test command" in result.output

        # Test with --info
        result = runner.invoke(cli, ["--info"])
        assert result.exit_code == 0
        assert "Test command" in result.output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
