rule ThreatLens_Test
{
    meta:
        description = "Detects a harmless test marker"

    strings:
        $test = "THREATLENS_TEST_SIGNATURE"

    condition:
        $test
}