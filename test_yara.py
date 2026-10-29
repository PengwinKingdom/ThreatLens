import yara

rules = yara.compile(filepath="rules/test_rule.yar")
matches = rules.match(filepath="sample.txt")

print("YARA matches:", [match.rule for match in matches])