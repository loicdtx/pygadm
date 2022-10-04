pyGADM
======

This library is a Python helper to download administrative boundaries data from the Database of **G**\ lobal **Adm**\ inistrative Areas (**GADM**) and load them in python memomy as :code:`GeoJson` like feature collections.

GADM provides maps and spatial data for all countries and their sub-divisions. The current version is 4.1 It delimits 400,276 administrative areas.  

Version 4.1 was released on 16 July 2022. New released are expected every three months. 
Older versions can be downloaded `here <https://gadm.org/old_versions.html>`__. More information can be found directly on the `GADM website <https://gadm.org/index.html>`__.

.. important::
   
   The data are freely available for academic use and other non-commercial use. Redistribution, or commercial use is not allowed without prior permission. See the license for more details. 

Install
-------

.. code-block:: console

    pip install git+https://github.com/loicdtx/pygadm.git


Examples
--------

.. code-block:: python

    from pprint import pprint
    import gadm

    # Download and load administrative boundaries of Mexico at municipality level (level 2 in GADM database)
    mex_fc = gadm.get_data(code='MEX', level=2)

    print(len(fc))
    # 1854

    # mex_fc is a FeatureCollection, it inherits from list and preserves all existing list methods
    print(type(mex_fc))
    # <class 'gadm.FeatureCollection'>

    # The FeatureCollection class has two methods: get and filter_by, to easily subset features collections
    # filter_by returns a FeatureCollection, so that multiple filter_by may be chained and eventually ended by
    # a get. This can be useful for instance in case there are multiple cities with the same name in different regions
    # of a country and you want to isolate a single one. get always return a single geojson like feature (dict).

    # Subset all municipalities of the state (NAME_1) of Oaxaca
    oax_fc = mex_fc.filter_by(NAME_1='Oaxaca')
    print(len(oax_fc))
    # 30

    # Get the feature of the municipality of Cuicatlan
    cui_feat = oax_fc.get(NAME_2='Cuicatlan')

    pprint(cui_feat)
    # {'geometry': {'coordinates': [[[(-96.9254531860351, 17.546520233154297),
    #                             (-96.92993164062494, 17.55500030517578),
    #                             (-96.93086242675781, 17.556520462036076),
    #                             (-96.93273162841797, 17.559141159057617),
    #                             ...
    #                             (-96.91992187499994, 17.54537963867199),
    #                             (-96.9254531860351, 17.546520233154297)]]],
    #           'type': 'MultiPolygon'},
    # 'id': '972',
    # 'properties': OrderedDict([('GID_0', 'MEX'),
    #                            ('NAME_0', 'Mexico'),
    #                            ('GID_1', 'MEX.20_1'),
    #                            ('NAME_1', 'Oaxaca'),
    #                            ('NL_NAME_1', None),
    #                            ('GID_2', 'MEX.20.3_1'),
    #                            ('NAME_2', 'Cuicatlan'),
    #                            ('VARNAME_2', 'Dist. Cuicatlan'),
    #                            ('NL_NAME_2', None),
    #                            ('TYPE_2', 'Municipio'),
    #                            ('ENGTYPE_2', 'Municipality'),
    #                            ('CC_2', None),
    #                            ('HASC_2', None)]),
    # 'type': 'Feature'}

    # If get does not hit any feature or hits more than one feature, it raises an exception
