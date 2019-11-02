#
# Conditional build:
%bcond_without	python		# Python extension

Summary:	CMU SphinxTrain - open source acoustic model trainer
Summary(pl.UTF-8):	CMU SpinxTrain - mający otwarte źródła trener modeli akustycznych
Name:		sphinxtrain
Version:	1.0.8
Release:	2
License:	BSD
Group:		Applications/Sound
Source0:	http://downloads.sourceforge.net/cmusphinx/%{name}-%{version}.tar.gz
# Source0-md5:	0f7155ba92fbdec169c92c1759303106
Patch0:		%{name}-update.patch
URL:		https://cmusphinx.github.io/
BuildRequires:	autoconf
BuildRequires:	automake
# C++11 required because of openfst
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtool >= 2:1.5
BuildRequires:	openfst-devel
BuildRequires:	opengrm-ngram-devel
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
%if %{with python}
BuildRequires:	python-Cython
BuildRequires:	python-devel >= 2.0
%endif
BuildRequires:	sphinxbase-devel >= 0.8
Requires:	python-numpy
Requires:	python-pyopenfst
Requires:	python-scipy
Requires:	python-sphinxbase >= 0.8
Requires:	sphinxbase >= 0.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is SphinxTrain, Carnegie Mellon University's open source acoustic
model trainer. This directory contains the scripts and instructions
necessary for building models for the CMU Sphinx Recognizer.

%description -l pl.UTF-8
PocketSphinx - jeden z pochodzących z Carnegie Mellon University,
mających otwarte źródła i bogaty zasób słów, niezależnych od mówiącego
silników rozpoznawania mowy ciągłej.

%package devel
Summary:	Header files for CMU SphinxTrain
Summary(pl.UTF-8):	Pliki nagłówkowe CMU SphinxTrain
Group:		Development/Libraries
Requires:	sphinxbase-devel >= 0.8
# doesn't require base currently

%description devel
Header files for CMU SphinxTrain.

%description devel -l pl.UTF-8
Pliki nagłówkowe CMU SphinxTrain.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e "s,/libexec/,/$(basename %{_libexec})/," scripts/sphinxtrain

%build
# rebuild ac/am/lt for as-needed to work
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
CXXFLAGS="%{rpmcxxflags} -std=c++11"
%configure \
	--enable-g2p-decoder \
	%{!?with_static_libs:--disable-static} \
	%{!?with_python:--without-python}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# not needed
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/sphinxtrain/python/setup.py \
	$RPM_BUILD_ROOT%{_libdir}/sphinxtrain/python/cmusphinx/{test,test_*.py} \
	$RPM_BUILD_ROOT%{_libdir}/sphinxtrain/scripts/lib/test_*

# not really executable
sed -i -e '1s,.*/usr/bin/env python.*,,' $RPM_BUILD_ROOT%{_libdir}/sphinxtrain/python/cmusphinx/lattice.py
# invoke python directly
sed -i -e '1s,/usr/bin/env python,%{__python},' $RPM_BUILD_ROOT%{_libdir}/sphinxtrain/python/cmusphinx/*.py

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING NEWS README
%attr(755,root,root) %{_bindir}/sphinxtrain
%if "%{_libexecdir}" != "%{_libdir}"
%dir %{_libexecdir}/sphinxtrain
%endif
%attr(755,root,root) %{_libexecdir}/sphinxtrain/agg_seg
%attr(755,root,root) %{_libexecdir}/sphinxtrain/bldtree
%attr(755,root,root) %{_libexecdir}/sphinxtrain/bw
%attr(755,root,root) %{_libexecdir}/sphinxtrain/cdcn_norm
%attr(755,root,root) %{_libexecdir}/sphinxtrain/cdcn_train
%attr(755,root,root) %{_libexecdir}/sphinxtrain/cp_parm
%attr(755,root,root) %{_libexecdir}/sphinxtrain/delint
%attr(755,root,root) %{_libexecdir}/sphinxtrain/g2p_train
%attr(755,root,root) %{_libexecdir}/sphinxtrain/inc_comp
%attr(755,root,root) %{_libexecdir}/sphinxtrain/init_gau
%attr(755,root,root) %{_libexecdir}/sphinxtrain/init_mixw
%attr(755,root,root) %{_libexecdir}/sphinxtrain/kdtree
%attr(755,root,root) %{_libexecdir}/sphinxtrain/kmeans_init
%attr(755,root,root) %{_libexecdir}/sphinxtrain/make_quests
%attr(755,root,root) %{_libexecdir}/sphinxtrain/map_adapt
%attr(755,root,root) %{_libexecdir}/sphinxtrain/mixw_interp
%attr(755,root,root) %{_libexecdir}/sphinxtrain/mk_flat
%attr(755,root,root) %{_libexecdir}/sphinxtrain/mk_mdef_gen
%attr(755,root,root) %{_libexecdir}/sphinxtrain/mk_mllr_class
%attr(755,root,root) %{_libexecdir}/sphinxtrain/mk_s2sendump
%attr(755,root,root) %{_libexecdir}/sphinxtrain/mk_ts2cb
%attr(755,root,root) %{_libexecdir}/sphinxtrain/mllr_solve
%attr(755,root,root) %{_libexecdir}/sphinxtrain/mllr_transform
%attr(755,root,root) %{_libexecdir}/sphinxtrain/norm
%attr(755,root,root) %{_libexecdir}/sphinxtrain/param_cnt
%attr(755,root,root) %{_libexecdir}/sphinxtrain/phonetisaurus-g2p
%attr(755,root,root) %{_libexecdir}/sphinxtrain/printp
%attr(755,root,root) %{_libexecdir}/sphinxtrain/prunetree
%attr(755,root,root) %{_libexecdir}/sphinxtrain/tiestate
%dir %{_libdir}/sphinxtrain
%{_libdir}/sphinxtrain/etc
%dir %{_libdir}/sphinxtrain/python
%dir %{_libdir}/sphinxtrain/python/cmusphinx
%{_libdir}/sphinxtrain/python/cmusphinx/feat
%attr(755,root,root) %{_libdir}/sphinxtrain/python/cmusphinx/classlm2fst.py
%attr(755,root,root) %{_libdir}/sphinxtrain/python/cmusphinx/cluster_mixw.py
%attr(755,root,root) %{_libdir}/sphinxtrain/python/cmusphinx/dict_spd.py
%attr(755,root,root) %{_libdir}/sphinxtrain/python/cmusphinx/fstutils.py
%attr(755,root,root) %{_libdir}/sphinxtrain/python/cmusphinx/lat2dot.py
%attr(755,root,root) %{_libdir}/sphinxtrain/python/cmusphinx/lat2fsg.py
%attr(755,root,root) %{_libdir}/sphinxtrain/python/cmusphinx/lat_rescore.py
%attr(755,root,root) %{_libdir}/sphinxtrain/python/cmusphinx/lat_rescore_fst.py
%attr(755,root,root) %{_libdir}/sphinxtrain/python/cmusphinx/lattice_conv.py
%attr(755,root,root) %{_libdir}/sphinxtrain/python/cmusphinx/lattice_error.py
%attr(755,root,root) %{_libdir}/sphinxtrain/python/cmusphinx/lattice_error_fst.py
%attr(755,root,root) %{_libdir}/sphinxtrain/python/cmusphinx/lattice_prune.py
%attr(755,root,root) %{_libdir}/sphinxtrain/python/cmusphinx/lda.py
%attr(755,root,root) %{_libdir}/sphinxtrain/python/cmusphinx/mllr.py
%attr(755,root,root) %{_libdir}/sphinxtrain/python/cmusphinx/mllt.py
%attr(755,root,root) %{_libdir}/sphinxtrain/python/cmusphinx/prune_mixw.py
%attr(755,root,root) %{_libdir}/sphinxtrain/python/cmusphinx/quantize_mixw.py
%attr(755,root,root) %{_libdir}/sphinxtrain/python/cmusphinx/sendump.py
%{_libdir}/sphinxtrain/python/cmusphinx/__init__.py
%{_libdir}/sphinxtrain/python/cmusphinx/arpalm.py
%{_libdir}/sphinxtrain/python/cmusphinx/corpus.py
%{_libdir}/sphinxtrain/python/cmusphinx/divergence.py
%{_libdir}/sphinxtrain/python/cmusphinx/evaluation.py
%{_libdir}/sphinxtrain/python/cmusphinx/gmm.py
%{_libdir}/sphinxtrain/python/cmusphinx/hmm.py
%{_libdir}/sphinxtrain/python/cmusphinx/htkmfc.py
%{_libdir}/sphinxtrain/python/cmusphinx/hypseg.py
%{_libdir}/sphinxtrain/python/cmusphinx/lattice.py
%{_libdir}/sphinxtrain/python/cmusphinx/mfcc.py
%{_libdir}/sphinxtrain/python/cmusphinx/qmwx.pyx
%{_libdir}/sphinxtrain/python/cmusphinx/s2mfc.py
%{_libdir}/sphinxtrain/python/cmusphinx/s3*.py
%dir %{_libdir}/sphinxtrain/scripts
%attr(755,root,root) %{_libdir}/sphinxtrain/scripts/[0-9]*
%attr(755,root,root) %{_libdir}/sphinxtrain/scripts/decode
%attr(755,root,root) %{_libdir}/sphinxtrain/scripts/prepare
%{_libdir}/sphinxtrain/scripts/lib

%files devel
%defattr(644,root,root,755)
%{_includedir}/sphinxtrain
