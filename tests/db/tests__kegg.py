from lrg_omics.db import kegg


def test__kegg_get_compound():
    kegg.get("C00058")


def test__kegg_get_enzyme():
    kegg.get("3.5.2.6")


def test__kegg_get_orthology():
    kegg.get("K18766")


def test__kegg_get_reaction():
    kegg.get("R01277")
