Name:           SuperLU
Version:        5.2.1
Release:        7
Summary:        Library for the direct solution of large, sparse, nonsymmetric systems of linear equations
License:        BSD and GPLv2+
URL:            http://crd-legacy.lbl.gov/~xiaoye/SuperLU/
Source0:        http://crd-legacy.lbl.gov/~xiaoye/SuperLU/superlu_%{version}.tar.gz
BuildRequires:  openblas-devel openblas-srpm-macros cmake3 gcc-gfortran csh
# Fixed include path for building
Patch0000:      superlu-cmake-includedir.patch
# Remove MC64 functionality
Patch0001:      superlu-removemc64.patch
# Add minor version for target properties
Patch0002:      SuperLU-5.2.1-set_soname.patch

%description
The library is written in C and is callable from either C or Fortran program. It uses MPI, OpenMP and
CUDA to support various forms of parallelism. It supports both real and complex datatypes, both single
and double precision, and 64-bit integer indexing. The library routines performs an LU decomposition
with partial pivoting and triangular system solves through forward and back substitution.

%package        devel
Summary:        Files for SuperLU development
Requires:       SuperLU = %{version}-%{release}

%description    devel
The package contains the header files and libraries for SuperLU development.

%package        help
Summary:        Documentation for SuperLU
Provides:       SuperLU-doc = %{version}-%{release}
Obsoletes:      SuperLU-doc < %{version}-%{release}
Requires:       SuperLU = %{version}-%{release}

%description    help
The package contains all the help documentation along with C and FORTRAN examples.

%prep
%autosetup -n SuperLU_%{version} -p1
rm -fr SRC/mc64ad.f.bak
find . -type f | sed -e "/TESTING/d" | xargs chmod a-x
find EXAMPLE -type f | while read file; do [ "$(file $file | awk '{print $2}')" = ELF ] && rm $file || : ; done
sed -i.bak '/NOOPTS/d' make.inc.in
sed -e 's|-O0|-O2|g' -i SRC/CMakeLists.txt

%build
mkdir -p build && cd build
%cmake3 -Denable_blaslib:BOOL=OFF -DCMAKE_BUILD_TYPE:STRING=Release ..
%make_build

%install
%make_install -C build

%check
cd build
ctest3 -V %{?_smp_mflags}
cd -

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc License.txt
%{_libdir}/libsuperlu.so.5*

%files devel
%{_includedir}/SuperLU/
%{_libdir}/libsuperlu.so

%files help
%doc DOC EXAMPLE FORTRAN

%changelog
* Fri Nov 19 2021 caodongxia <caodongxia@huawei.com> - 5.2.1-7
- Remove useless buildRequire:atlas-devel

* Thu Mar 5 2020 Ling Yang <lingyang2@huawei.com> - 5.2.1-6
- Package Init
