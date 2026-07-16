"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : Source Priority
Purpose : Define trusted sources for each field
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
"""

FIELD_PRIORITY = {

    "province": [
        "Wikipedia",
        "Pindula",
        "ZimbabweYP",
        "OpenClass",
        "IBZIM"
    ],

    "city": [
        "Wikipedia",
        "Pindula",
        "ZimbabweYP",
        "OpenClass",
        "IBZIM"
    ],

    "physical_address": [
        "ZimbabweYP",
        "Pindula",
        "Wikipedia",
        "OpenClass",
        "IBZIM"
    ],

    "phone_numbers": [
        "ZimbabweYP",
        "Pindula",
        "Wikipedia",
        "OpenClass",
        "IBZIM"
    ],

    "website": [
        "ZimbabweYP",
        "Wikipedia",
        "Pindula",
        "OpenClass",
        "IBZIM"
    ],

    "ranking_o_level": [
        "IBZIM"
    ],

    "ranking_a_level": [
        "IBZIM"
    ]
}