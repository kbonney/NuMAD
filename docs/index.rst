.. _home:

.. figure:: /_static/images/NuMAD-header.png
   :target: https://github.com/sandialabs/NuMAD


##################################################################################
Numerical Manufacturing And Design (NuMAD) Tool for Wind Turbine Blades
##################################################################################

.. toctree::
   :maxdepth: 2
   :hidden:
   
   Home <self>
   introduction/index.rst
   gettingstarted.rst
   userguide/index.rst
   API documentation <apidoc/pynumad>
   developer.rst


The structural design and optimization of wind turbine blades is a
complex task. In many cases it is difficult to find the optimal design
of a turbine blade by hand, or by trial and error, and the software
tools used for such designs are most effective when integrated into
automated optimization and analysis algorithms. A new version of the
software tool  for the design
and modeling of wind turbine blades is developed and described. 

PyNuMAD is the Python release of `NuMAD (Numerical Manufacturing And Design) <https://github.com/sandialabs/NuMAD>`_,
a matlab-based tool designed to facilitate the design process for wind turbine blades. 
PyNuMAD is an object-oriented package structured to be run in a scripting environment.
Releasing a version of NuMAD in Python is a part of
an effort by the development team to bring NuMAD into a FOSS environment by reducing license requirements. Another part of this effort
is the development of an in-house meshing tool. Previously, the creation of a blade mesh was done in an external tool like ANSYS, but now
pyNuMAD implements this functionality.
Major features include:

   - I/O for common blade ontologies (WindIO yaml, Excel).
   - Management of blade geometry and materials.
   - Built-in shell and brick mesher.
   - Integration with external codes


.. _developers:

NuMAD Developers
=====================
NuMAD has been developed by `Sandia National Laboratories 
(Sandia) <https://energy.sandia.gov/programs/renewable-energy/wind-power/>`_, 
funded by the U.S. Department of Energy’s Wind Energy Technologies Technologies Office. 


Current members of the development team include:

* Joshua Paquette (“Josh”) (Sandia - PI)
* Evan Anderson (Sandia)
* Ernesto Camarena (Sandia)
* Ryan James Clarke (Sandia)
* Kirk Bonney (Sandia)

Former members of the development team include:

* Jonathan Charles Berg
* Brian Resor
* Daniel Laird
* Kelley Ruehl (Sandia)
* Christopher Lee Kelley (Sandia)
* Brandon Lee Ennis (Sandia)

Funding
=======

Development and maintenance of the NuMAD code is funded by the U.S. Department of Energy’s Wind Energy Technologies Office.

Sandia National Laboratories is a multi-mission laboratory managed and operated by 
National Technology and Engineering Solutions of Sandia, LLC., a wholly owned subsidiary 
of Honeywell International, Inc., for the U.S. Department of Energy’s National Nuclear 
Security Administration under contract DE-NA0003525.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
