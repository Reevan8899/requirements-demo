const reqTypes = new Set(["feat", "fix", "test"]);
const reqSuffix = /\((?:(?:BR|UR|FR|NFR)-\d{3})(?:, (?:BR|UR|FR|NFR)-\d{3})*\)$/;

module.exports = {
  extends: ["@commitlint/config-conventional"],
  plugins: [{
    rules: {
      "requirement-id": ({ type, subject }) => [
        !reqTypes.has(type) || reqSuffix.test(subject || ""),
        "Для feat, fix и test укажите ID требования в конце темы, например (FR-001).",
      ],
    },
  }],
  rules: {
    "requirement-id": [2, "always"],
    "header-max-length": [2, "always", 160],
    "type-enum": [2, "always", ["build", "chore", "ci", "docs", "feat", "fix", "perf", "refactor", "revert", "style", "test"]],
  },
};
