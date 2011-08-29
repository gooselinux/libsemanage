%define libsepolver 2.0.37-1
%define libselinuxver 2.0.0-1
Summary: SELinux binary policy manipulation library 
Name: libsemanage
Version: 2.0.43
Release: 4%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
Source: http://www.nsa.gov/selinux/archives/libsemanage-%{version}.tgz
Patch: libsemanage-rhat.patch
URL: http://www.selinuxproject.org

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libselinux-devel >= %{libselinuxver} swig ustr-devel
BuildRequires: libsepol-devel >= %{libsepolver} 
BuildRequires: python-devel bison flex bzip2-devel
Requires: bzip2-libs

%description
Security-enhanced Linux is a feature of the Linux® kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux.  The Security-enhanced Linux
kernel contains new architectural components originally developed to
improve the security of the Flask operating system. These
architectural components provide general support for the enforcement
of many kinds of mandatory access control policies, including those
based on the concepts of Type Enforcement®, Role-based Access
Control, and Multi-level Security.

libsemanage provides an API for the manipulation of SELinux binary policies.
It is used by checkpolicy (the policy compiler) and similar tools, as well
as by programs like load_policy that need to perform specific transformations
on binary policies such as customizing policy boolean settings.

%package static
Summary: Static library used to build policy manipulation tools
Group: Development/Libraries
Requires: libsemanage-devel = %{version}-%{release}

%description static
The semanage-static package contains the static libraries 
needed for developing applications that manipulate binary policies. 

%package devel
Summary: Header files and libraries used to build policy manipulation tools
Group: Development/Libraries
Requires: libsemanage = %{version}-%{release} ustr

%description devel
The semanage-devel package contains the libraries and header files
needed for developing applications that manipulate binary policies. 

%package python
Summary: semanage python bindings for libsemanage
Group: Development/Libraries
Requires: libsemanage = %{version}-%{release} 

%description python
The libsemanage-python package contains the python bindings for developing 
SELinux management applications. 

%prep
%setup -q
%patch -p1 -b .rhat

%build
make clean
make CFLAGS="%{optflags}" swigify
make CFLAGS="%{optflags}" LIBDIR="%{_libdir}" SHLIBDIR="%{_lib}" all pywrap


%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/%{_lib} 
mkdir -p ${RPM_BUILD_ROOT}/%{_libdir} 
mkdir -p ${RPM_BUILD_ROOT}%{_includedir} 
make DESTDIR="${RPM_BUILD_ROOT}" LIBDIR="${RPM_BUILD_ROOT}%{_libdir}" SHLIBDIR="${RPM_BUILD_ROOT}/%{_lib}" install install-pywrap
ln -sf  /%{_lib}/libsemanage.so.1 ${RPM_BUILD_ROOT}/%{_libdir}/libsemanage.so

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%config(noreplace) /etc/selinux/semanage.conf
/%{_lib}/libsemanage.so.1

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files static
%defattr(-,root,root)
%{_libdir}/libsemanage.a

%files devel
%defattr(-,root,root)
%{_libdir}/libsemanage.so
%{_libdir}/pkgconfig/libsemanage.pc
%dir %{_includedir}/semanage
%{_includedir}/semanage/*.h
%{_mandir}/man3/*

%files python
%defattr(-,root,root)
%{_libdir}/python*/site-packages/*

%changelog
* Thu Jan 28 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.43-4
- Cleanup spec file
Resolves: #555835

* Mon Jan 18 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.43-3
- Splect libsemanage.a into a static subpackage to keep fedora packaging guidelines happy

* Wed Dec 16 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.43-2
- Rebuild all c programs with -fPIC

* Tue Dec 1 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.43-1
- Update to upstream
  * Move libsemanage.so to /usr/lib
  * Add NAME lines to man pages from Manoj Srivastava<srivasta@debian.org>

* Wed Nov 18 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.42-1
- Update to upstream
  * Move load_policy from /usr/sbin to /sbin from Dan Walsh.

* Mon Nov 2 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.41-1
- Update to upstream
  * Add pkgconfig file from Eamon Walsh.
  * Add semanage_set_check_contexts() function to disable calling
  setfiles

* Mon Sep 28 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.39-1
- Update to upstream
  * make swigify

* Sun Sep 20 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.38-2
- Dont relabel /root with genhomedircon

* Thu Sep 17 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.38-1
- Update to upstream
  * Change semodule upgrade behavior to install even if the module
    is not present from Dan Walsh.
  * Make genhomedircon trim excess '/' from homedirs from Dan Walsh.

* Wed Sep 9 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.37-1
- Update to upstream
  * Fix persistent dontaudit support to rebuild policy if the 
        dontaudit state is changed from Chad Sellers.
- Move load_policy to /sbin

* Fri Aug 28 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.36-2
- Add enable/disable modules

* Wed Aug 26 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.36-1
- Update to upstream
  * Changed bzip-blocksize=0 handling to support existing compressed
  modules in the store.

* Wed Aug 26 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.35-2
- Make sure /root is not used in genhomedircon

* Wed Aug 5 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.35-1
  * Revert hard linking of files between tmp/active/previous.
  * Enable configuration of bzip behavior from Stephen Smalley.
    bzip-blocksize=0 to disable compression and decompression support.
    bzip-blocksize=1..9 to set the blocksize for compression.
    bzip-small=true to reduce memory usage for decompression.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 10 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.33-2
- Put check for /root back into genhomedircon

* Tue Jul 7 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.33-1
- Update to upstream

* Mon Jun 8 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.32-1
- Update to upstream
  * Ruby bindings from David Quigley.

* Thu Apr 9 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.31-5
- Return error on invalid file

* Wed Mar 11 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.31-4
- Fix typo

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.31-2
- Fix link to only link on sandbox

* Mon Jan 12 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.31-1
- Update to upstream
  * Policy module compression (bzip) support from Dan Walsh.
  * Hard link files between tmp/active/previous from Dan Walsh.

* Mon Jan 12 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.30-3
- Fix up patch to get it upstreamed

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.30-2
- Rebuild for Python 2.6

* Thu Dec 4 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.30-1
  * Add semanage_mls_enabled() interface from Stephen Smalley.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.29-2
- Rebuild for Python 2.6

* Mon Sep 15 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.28-1
- Update to upstream
  * Add USER to lines to homedir_template context file from Chris PeBenito.

* Mon Sep 15 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.28-2
- Add compression support

* Mon Sep 15 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.28-1
- Update to upstream
  * allow fcontext and seuser changes without rebuilding the policy from Dan Walsh

* Wed Sep 10 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.27-3
- Additional fixes for Don't rebuild on fcontext or seuser modifications

* Tue Sep 2 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.27-2
- Don't rebuild on fcontext or seuser modifications

* Tue Aug 5 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.27-1
- Update to upstream
  * Modify genhomedircon to skip groupname entries.
  Ultimately we need to expand them to the list of users to support per-role homedir labeling when using the groupname syntax.

* Wed Jul 29 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.26-1
- Update to upstream
  * Fix bug in genhomedircon fcontext matches logic from Dan Walsh.
  Strip any trailing slash before appending /*$.

* Thu Jun 17 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.25-3
- Another fix for genhomedircon

* Wed May 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.25-2
- fix license tag

* Tue Feb 5 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.25-1
- Update to upstream
  * Do not call genhomedircon if the policy was not rebuilt from Stephen Smalley.
    Fixes semanage boolean -D seg fault (bug 441379).

* Tue Feb 5 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.24-1
- Update to upstream
  * make swigify

* Tue Feb 5 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.23-1
- Update to upstream
  * Use vfork rather than fork for libsemanage helpers to reduce memory overhead as suggested by Todd Miller.

* Mon Feb 4 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.22-1
- Update to upstream
  * Free policydb before fork from Joshua Brindle.
  * Drop the base module immediately after expanding to permit memory re-use from Stephen Smalley.

* Sat Feb 2 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.20-1
- Update to upstream
  * Use sepol_set_expand_consume_base to reduce peak memory usage when
  using semodule

* Fri Feb 1 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.19-1
- Update to upstream
  * Fix genhomedircon to not override a file context with a homedir context from Todd Miller.

* Tue Jan 29 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.18-1
- Update to upstream
  * Fix spurious out of memory error reports.
  * Merged second version of fix for genhomedircon handling from Caleb Case.

* Tue Jan 22 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.16-1
- Update to upstream
  * Merged fix for genhomedircon handling of missing HOME_DIR or HOME_ROOT templates from Caleb Case.

* Tue Jan 22 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.15-2
- Stop differentiating on user for homedir labeling

* Thu Dec 6 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.15-1
- Update to upstream
  * Fix genhomedircon handling of shells and missing user context template from Dan Walsh.
  * Copy the store path in semanage_select_store from Dan Walsh.
- Add expand-check=0 to semanage.conf

* Mon Dec 3 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.14-5
- Fix handling of /etc/shells so genhomedircon will work

* Thu Nov 29 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.14-3
- Allow semanage_genhomedircon to work with out a USER int homedir.template

* Sat Nov 10 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.14-2
- Fix semanage_select_store to allocate memory, fixes crash on invalid store

* Tue Nov 6 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.14-1
- Upgrade to latest from NSA
  * Call rmdir() rather than remove() on directory removal so that errno isn't polluted from Stephen Smalley.
  * Allow handle_unknown in base to be overridden by semanage.conf from Stephen Smalley.

* Fri Oct 5 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.12-1
- Upgrade to latest from NSA
  * ustr cleanups from James Antill.
  * Ensure that /root gets labeled even if using the default context from Dan Walsh.

* Fri Sep 28 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.11-1
- Upgrade to latest from NSA
  * Fix ordering of file_contexts.homedirs from Todd Miller and Dan Walsh.

* Fri Sep 28 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.10-2
- Fix sort order on generated homedir context

* Fri Sep 28 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.10-1
- Upgrade to latest from NSA
  * Fix error checking on getpw*_r functions from Todd Miller.
  * Make genhomedircon skip invalid homedir contexts from Todd Miller.
  * Set default user and prefix from seusers from Dan Walsh.
  * Add swigify Makefile target from Dan Walsh.

* Wed Sep 26 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.9-1
- Upgrade to latest from NSA
  * Pass CFLAGS to CC even on link command, per Dennis Gilmore.
  * Clear errno on non-fatal errors to avoid reporting them upon a
    later error that does not set errno.
  * Improve reporting of system errors, e.g. full filesystem or read-only filesystem from Stephen Smalley.

- Fix segfault in genhomedircon when using bad user names

* Wed Sep 26 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.6-2
- Fix genhomedircon code to only generate valid context
- Fixes autorelabel problem

* Thu Sep 13 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.6-1
- Upgrade to latest from NSA
  * Change to use getpw* function calls to the _r versions from Todd Miller.

* Thu Aug 23 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.5-1
- Upgrade to latest from NSA

* Mon Aug 20 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.4-1
- Upgrade to latest from NSA
  * Allow dontaudits to be turned off via semanage interface when
    updating policy

* Sat Aug 11 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.3-5
- Add ability to load a policy without dontaudit rules
-

* Tue Jun 26 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.3-4
- Rebuild to fix segfault on x86 platforms, swigify on each build

* Fri Jun 1 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.3-3
- Rebuild for rawhide

* Thu May 3 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.3-2
- Apply patch to fix dependencies in spec file from Robert Scheck

* Wed Apr 25 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.3-1
- Upgrade to latest from NSA
  * Fix to libsemanage man patches so whatis will work better from Dan Walsh

* Wed Apr 25 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.2-1
- Upgrade to latest from NSA
  * Merged optimizations from Stephen Smalley.
    - do not set all booleans upon commit, only those whose values have changed
    - only install the sandbox upon commit if something was rebuilt

* Sat Mar 17 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.1-2
- Add SELinux to Man page Names so man -k will work

* Mon Mar 12 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.1-1
  * Merged dbase_file_flush patch from Dan Walsh.
    This removes any mention of specific tools (e.g. semanage)
    from the comment header of the auto-generated files,
    since there are multiple front-end tools.

* Tue Feb 20 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.0-1
- Upgrade to latest from NSA
  * Merged Makefile test target patch from Caleb Case.
  * Merged get_commit_number function rename patch from Caleb Case.
  * Merged strnlen -> strlen patch from Todd Miller.

* Wed Feb 7 2007 Dan Walsh <dwalsh@redhat.com> - 1.10.1-1
- Upgrade to latest from NSA
  * Merged python binding fix from Dan Walsh.
  * Updated version for stable branch.

* Fri Dec 22 2006 Dan Walsh <dwalsh@redhat.com> - 1.9.2-1
- Upgrade to latest from NSA
  * Merged patch to optionally reduce disk usage by removing 
    the backup module store and linked policy from Karl MacMillan
  * Merged patch to correctly propagate return values in libsemanage

* Fri Dec 22 2006 Dan Walsh <dwalsh@redhat.com> - 1.9.1-3
- Apply Karl MacMillan patch to get proper error codes.

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 1.9.1-2
- rebuild against python 2.5

* Tue Nov 28 2006 Dan Walsh <dwalsh@redhat.com> - 1.9.1-1
- Upgrade to latest from NSA
  * Merged patch to compile wit -fPIC instead of -fpic from
    Manoj Srivastava to prevent hitting the global offest table
    limit. Patch changed to include libselinux and libsemanage in
    addition to libsepol.

* Tue Oct 17 2006 Dan Walsh <dwalsh@redhat.com> - 1.8-1
- Upgrade to latest from NSA
  * Updated version for release.

* Thu Aug 31 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.17-1
- Upgrade to latest from NSA
  * Merged patch to skip reload if no active store exists and
    the store path doesn't match the active store path from Dan Walsh.
  * Merged patch to not destroy sepol handle on error path of
    connect from James Athey.
  * Merged patch to add genhomedircon path to semanage.conf from
    James Athey. 

* Thu Aug 31 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.16-3
- Fix semanage to not load if is not the correct policy type and it is installing

* Thu Aug 31 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.16-2
- Fix requires lines

* Wed Aug 23 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.16-1
- Upgrade to latest from NSA
  * Make most copy errors fatal, but allow exceptions for
    file_contexts.local, seusers, and netfilter_contexts if
    the source file does not exist in the store.

* Sat Aug 12 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.15-1
- Upgrade to latest from NSA
  * Merged separate local file contexts patch from Chris PeBenito.
  * Merged patch to make most copy errors non-fatal from Dan Walsh.

* Thu Aug 10 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.13-3
- Change other updates to be non-fatal

* Wed Aug 9 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.13-2
- Change netfilter stuff to be non-fatal so update can proceed.

* Thu Aug 3 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.13-1
- Upgrade to latest from NSA
  * Merged netfilter contexts support from Chris PeBenito.

* Mon Jul 17 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.12-2
- Rebuild for new gcc

* Tue Jul 11 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.12-1
- Upgrade to latest from NSA
  * Merged support for read operations on read-only fs from 
    Caleb Case (Tresys Technology).

* Tue Jul 4 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.11-1
- Upgrade to latest from NSA
  * Lindent.
  * Merged setfiles location check patch from Dan Walsh.

* Fri Jun 16 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.9-1
- Upgrade to latest from NSA
  * Merged several fixes from Serge Hallyn:
       dbase_file_cache:  deref of uninit data on error path.
       dbase_policydb_cache:  clear fp to avoid double fclose
       semanage_fc_sort:  destroy temp on error paths

* Fri Jun 16 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.8-2
- Handle setfiles being in /sbin or /usr/sbin

* Mon May 15 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.8-1
- Upgrade to latest from NSA
  * Updated default location for setfiles to /sbin to
    match policycoreutils.  This can also be adjusted via 
    semanage.conf using the syntax:
    [setfiles]
    path = /path/to/setfiles
    args = -q -c $@ $<
    [end]

* Mon May 15 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.7-3
- Spec file cleanup from n0dalus+redhat@gmail.com

* Mon May 15 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.7-2
- Add /usr/include/semanage to spec file

* Mon May 8 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.7-1
- Upgrade to latest from NSA
  * Merged fix warnings patch from Karl MacMillan.

* Fri Apr 14 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.6-1
- Upgrade to latest from NSA
  * Merged updated file context sorting patch from Christopher
    Ashworth, with bug fix for escaped character flag.
  * Merged file context sorting code from Christopher Ashworth 
    (Tresys Technology), based on fc_sort.c code in refpolicy.
  * Merged python binding t_output_helper removal patch from Dan Walsh.
  * Regenerated swig files.

* Wed Mar 29 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.3-1
- Fix to work with new version of swig
- Upgrade to latest from NSA
  * Merged corrected fix for descriptor leak from Dan Walsh.

* Wed Mar 29 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.2-2
- Fix leaky descriptor

* Tue Mar 21 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.2-1
- Upgrade to latest from NSA
  * Merged Makefile PYLIBVER definition patch from Dan Walsh.
  * Merged man page reorganization from Ivan Gyurdiev.

* Fri Mar 17 2006 Dan Walsh <dwalsh@redhat.com> - 1.6-1
- Make work on RHEL4
- Upgrade to latest from NSA
  * Merged abort early on merge errors patch from Ivan Gyurdiev.
  * Cleaned up error handling in semanage_split_fc based on a patch
    by Serge Hallyn (IBM) and suggestions by Ivan Gyurdiev.
  * Merged MLS handling fixes from Ivan Gyurdiev.

* Fri Feb 17 2006 Dan Walsh <dwalsh@redhat.com> - 1.5.28-1
- Upgrade to latest from NSA
  * Merged bug fix for fcontext validate handler from Ivan Gyurdiev.
  * Merged base_merge_components changes from Ivan Gyurdiev.

* Thu Feb 16 2006 Dan Walsh <dwalsh@redhat.com> - 1.5.26-1
- Upgrade to latest from NSA
  * Merged paths array patch from Ivan Gyurdiev.
  * Merged bug fix patch from Ivan Gyurdiev.
  * Merged improve bindings patch from Ivan Gyurdiev.
  * Merged use PyList patch from Ivan Gyurdiev.  
  * Merged memory leak fix patch from Ivan Gyurdiev.
  * Merged nodecon support patch from Ivan Gyurdiev.
  * Merged cleanups patch from Ivan Gyurdiev.
  * Merged split swig patch from Ivan Gyurdiev.

* Mon Feb 13 2006 Dan Walsh <dwalsh@redhat.com> - 1.5.23-1
- Upgrade to latest from NSA
  * Merged optionals in base patch from Joshua Brindle.
  * Merged treat seusers/users_extra as optional sections patch from
    Ivan Gyurdiev.
  * Merged parse_optional fixes from Ivan Gyurdiev.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.5.21-2.1
- bump again for double-long bug on ppc(64)

* Fri Feb 10 2006 Dan Walsh <dwalsh@redhat.com> - 1.5.21-2
- Fix handling of seusers and users_map file

* Tue Feb 07 2006 Dan Walsh <dwalsh@redhat.com> - 1.5.21-1
- Upgrade to latest from NSA
  * Merged seuser/user_extra support patch from Joshua Brindle.
  * Merged remote system dbase patch from Ivan Gyurdiev.  

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.5.20-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb 2 2006 Dan Walsh <dwalsh@redhat.com> 1.5.20-1
- Upgrade to latest from NSA
  * Merged clone record on set_con patch from Ivan Gyurdiev.  

* Mon Jan 30 2006 Dan Walsh <dwalsh@redhat.com> 1.5.19-1
- Upgrade to latest from NSA
  * Merged fname parameter patch from Ivan Gyurdiev.
  * Merged more size_t -> unsigned int fixes from Ivan Gyurdiev.
  * Merged seusers.system patch from Ivan Gyurdiev.
  * Merged improve port/fcontext API patch from Ivan Gyurdiev.  

* Fri Jan 27 2006 Dan Walsh <dwalsh@redhat.com> 1.5.18-1
- Upgrade to latest from NSA
  * Merged seuser -> seuser_local rename patch from Ivan Gyurdiev.
  * Merged set_create_store, access_check, and is_connected interfaces
    from Joshua Brindle.

* Fri Jan 13 2006 Dan Walsh <dwalsh@redhat.com> 1.5.16-1
- Upgrade to latest from NSA
  * Regenerate python wrappers.

* Fri Jan 13 2006 Dan Walsh <dwalsh@redhat.com> 1.5.15-1
- Upgrade to latest from NSA
  * Merged pywrap Makefile diff from Dan Walsh.
  * Merged cache management patch from Ivan Gyurdiev.
  * Merged bugfix for dbase_llist_clear from Ivan Gyurdiev.
  * Merged remove apply_local function patch from Ivan Gyurdiev.
  * Merged only do read locking in direct case patch from Ivan Gyurdiev.
  * Merged cache error path memory leak fix from Ivan Gyurdiev.
  * Merged auto-generated file header patch from Ivan Gyurdiev.
  * Merged pywrap test update from Ivan Gyurdiev.
  * Merged hidden defs update from Ivan Gyurdiev.

* Fri Jan 13 2006 Dan Walsh <dwalsh@redhat.com> 1.5.14-2
- Break out python out of regular Makefile

* Fri Jan 13 2006 Dan Walsh <dwalsh@redhat.com> 1.5.14-1
- Upgrade to latest from NSA
  * Merged disallow port overlap patch from Ivan Gyurdiev.
  * Merged join prereq and implementation patches from Ivan Gyurdiev.
  * Merged join user extra data part 2 patch from Ivan Gyurdiev.
  * Merged bugfix patch from Ivan Gyurdiev.
  * Merged remove add_local/set_local patch from Ivan Gyurdiev.
  * Merged user extra data part 1 patch from Ivan Gyurdiev.
  * Merged size_t -> unsigned int patch from Ivan Gyurdiev.
  * Merged calloc check in semanage_store patch from Ivan Gyurdiev,
    bug noticed by Steve Grubb.
  * Merged cleanups after add/set removal patch from Ivan Gyurdiev.

* Fri Jan 7 2006 Dan Walsh <dwalsh@redhat.com> 1.5.9-1
- Upgrade to latest from NSA
  * Merged const in APIs patch from Ivan Gyurdiev.
  * Merged validation of local file contexts patch from Ivan Gyurdiev.
  * Merged compare2 function patch from Ivan Gyurdiev.
  * Merged hidden def/proto update patch from Ivan Gyurdiev.

* Thu Jan 6 2006 Dan Walsh <dwalsh@redhat.com> 1.5.8-1
- Upgrade to latest from NSA
  * Re-applied string and file optimization patch from Russell Coker,
    with bug fix.
  * Reverted string and file optimization patch from Russell Coker.
  * Clarified error messages from parse_module_headers and 
    parse_base_headers for base/module mismatches.

* Thu Jan 6 2006 Dan Walsh <dwalsh@redhat.com> 1.5.6-1
- Upgrade to latest from NSA
  * Clarified error messages from parse_module_headers and 
    parse_base_headers for base/module mismatches.
  * Merged string and file optimization patch from Russell Coker.
  * Merged swig header reordering patch from Ivan Gyurdiev.
  * Merged toggle modify on add patch from Ivan Gyurdiev.
  * Merged ports parser bugfix patch from Ivan Gyurdiev.
  * Merged fcontext swig patch from Ivan Gyurdiev.
  * Merged remove add/modify/delete for active booleans patch from Ivan Gyurdiev.
  * Merged man pages for dbase functions patch from Ivan Gyurdiev.
  * Merged pywrap tests patch from Ivan Gyurdiev.

* Wed Jan 5 2006 Dan Walsh <dwalsh@redhat.com> 1.5.4-2
- Patch to fix add

* Wed Jan 5 2006 Dan Walsh <dwalsh@redhat.com> 1.5.4-1
- Upgrade to latest from NSA
  * Merged patch series from Ivan Gyurdiev.
    This includes patches to:
    - separate file rw code from linked list
    - annotate objects
    - fold together internal headers
    - support ordering of records in compare function
    - add active dbase backend, active booleans
    - return commit numbers for ro database calls
    - use modified flags to skip rebuild whenever possible
    - enable port interfaces
    - update swig interfaces and typemaps
    - add an API for file_contexts.local and file_contexts
    - flip the traversal order in iterate/list
    - reorganize sandbox_expand
    - add seusers MLS validation
    - improve dbase spec/documentation
    - clone record on set/add/modify

* Tue Dec 27 2005 Dan Walsh <dwalsh@redhat.com> 1.5.3-3
- Add Ivans patch to turn on ports

* Wed Dec 14 2005 Dan Walsh <dwalsh@redhat.com> 1.5.3-2
- Remove patch since upstream does the right thing

* Wed Dec 14 2005 Dan Walsh <dwalsh@redhat.com> 1.5.3-1
- Upgrade to latest from NSA
  * Merged further header cleanups from Ivan Gyurdiev.
  * Merged toggle modified flag in policydb_modify, fix memory leak
    in clear_obsolete, polymorphism vs headers fix, and include guards
    for internal headers patches from Ivan Gyurdiev.

* Tue Dec 13 2005 Dan Walsh <dwalsh@redhat.com> 1.5.1-2
- Upgrade to latest from NSA
  * Merged toggle modified flag in policydb_modify, fix memory leak
    in clear_obsolete, polymorphism vs headers fix, and include guards
    for internal headers patches from Ivan Gyurdiev.

* Mon Dec 12 2005 Dan Walsh <dwalsh@redhat.com> 1.5.1-1
- Upgrade to latest from NSA
  * Added file-mode= setting to semanage.conf, default to 0644.
    Changed semanage_copy_file and callers to use this mode when
    installing policy files to runtime locations.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Dec 7 2005 Dan Walsh <dwalsh@redhat.com> 1.4-1
- Fix mode of output seusers file

* Tue Dec 6 2005 Dan Walsh <dwalsh@redhat.com> 1.3.64-1
- Upgrade to latest from NSA
  * Changed semanage_handle_create() to set do_reload based on
    is_selinux_enabled().  This prevents improper attempts to
    load policy on a non-SELinux system.

* Mon Dec 5 2005 Dan Walsh <dwalsh@redhat.com> 1.3.63-1
- Upgrade to latest from NSA
  * Dropped handle from user_del_role interface.
  * Removed defrole interfaces.

* Tue Nov 29 2005 Dan Walsh <dwalsh@redhat.com> 1.3.61-1
- Upgrade to latest from NSA
  * Merged Makefile python definitions patch from Dan Walsh.
  * Removed is_selinux_mls_enabled() conditionals in seusers and users
    file parsers. 

* Wed Nov 23 2005 Dan Walsh <dwalsh@redhat.com> 1.3.59-1
- Add additional swig objects
  * Merged wrap char*** for user_get_roles patch from Joshua Brindle.
  * Merged remove defrole from sepol patch from Ivan Gyurdiev.
  * Merged swig wrappers for modifying users and seusers from Joshua Brindle.

* Wed Nov 23 2005 Dan Walsh <dwalsh@redhat.com> 1.3.56-2
- Add additional swig objects

* Fri Nov 16 2005 Dan Walsh <dwalsh@redhat.com> 1.3.56-1
- Upgrade to latest from NSA
  * Fixed free->key_free bug.
  * Merged clear obsolete patch from Ivan Gyurdiev.
  * Merged modified swigify patch from Dan Walsh 
    (original patch from Joshua Brindle).
  * Merged move genhomedircon call patch from Chad Sellers.

* Mon Nov 14 2005 Dan Walsh <dwalsh@redhat.com> 1.3.53-3
- Add genhomedircon patch from Joshua Brindle

* Fri Nov 11 2005 Dan Walsh <dwalsh@redhat.com> 1.3.53-2
- Add swigify patch from Joshua Brindle

* Fri Nov 11 2005 Dan Walsh <dwalsh@redhat.com> 1.3.53-1
- Upgrade to latest from NSA
  * Merged move seuser validation patch from Ivan Gyurdiev.
  * Merged hidden declaration fixes from Ivan Gyurdiev,
    with minor corrections.

* Wed Nov 9 2005 Dan Walsh <dwalsh@redhat.com> 1.3.52-1
- Upgrade to latest from NSA
  * Merged cleanup patch from Ivan Gyurdiev.
    This renames semanage_module_conn to semanage_direct_handle,
    and moves sepol handle create/destroy into semanage handle
    create/destroy to allow use even when disconnected (for the
    record interfaces).

* Tue Nov 8 2005 Dan Walsh <dwalsh@redhat.com> 1.3.51-1
- Upgrade to latest from NSA
  * Clear modules modified flag upon disconnect and commit.
        * Added tracking of module modifications and use it to
    determine whether expand-time checks should be applied
    on commit.
  * Reverted semanage_set_reload_bools() interface.

* Tue Nov 8 2005 Dan Walsh <dwalsh@redhat.com> 1.3.48-1
- Upgrade to latest from NSA
  * Disabled calls to port dbase for merge and commit and stubbed
    out calls to sepol_port interfaces since they are not exported.
  * Merged rename instead of copy patch from Joshua Brindle (Tresys).
  * Added hidden_def/hidden_proto for exported symbols used within 
    libsemanage to eliminate relocations.  Wrapped type definitions
    in exported headers as needed to avoid conflicts.  Added
    src/context_internal.h and src/iface_internal.h.
  * Added semanage_is_managed() interface to allow detection of whether
    the policy is managed via libsemanage.  This enables proper handling
    in setsebool for non-managed systems.
  * Merged semanage_set_reload_bools() interface from Ivan Gyurdiev,
    to enable runtime control over preserving active boolean values
    versus reloading their saved settings upon commit.

* Mon Nov 7 2005 Dan Walsh <dwalsh@redhat.com> 1.3.43-1
- Upgrade to latest from NSA
  * Merged seuser parser resync, dbase tracking and cleanup, strtol
    bug, copyright, and assert space patches from Ivan Gyurdiev.
  * Added src/*_internal.h in preparation for other changes.
   * Added hidden/hidden_proto/hidden_def to src/debug.[hc] and
          src/seusers.[hc].


* Thu Nov 3 2005 Dan Walsh <dwalsh@redhat.com> 1.3.41-1
- Upgrade to latest from NSA
  * Merged interface parse/print, context_to_string interface change,
    move assert_noeof, and order preserving patches from Ivan Gyurdiev.
        * Added src/dso.h in preparation for other changes.
  * Merged install seusers, handle/error messages, MLS parsing,
    and seusers validation patches from Ivan Gyurdiev.

* Mon Oct 31 2005 Dan Walsh <dwalsh@redhat.com> 1.3.39-1
- Upgrade to latest from NSA
  * Merged record interface, dbase flush, common database code,
    and record bugfix patches from Ivan Gyurdiev.

* Fri Oct 28 2005 Dan Walsh <dwalsh@redhat.com> 1.3.38-1
- Upgrade to latest from NSA
  * Merged dbase policydb list and count change from Ivan Gyurdiev.
  * Merged enable dbase and set relay patches from Ivan Gyurdiev.

* Thu Oct 27 2005 Dan Walsh <dwalsh@redhat.com> 1.3.36-1
- Update from NSA
  * Merged query APIs and dbase_file_set patches from Ivan Gyurdiev.

* Wed Oct 26 2005 Dan Walsh <dwalsh@redhat.com> 1.3.35-1
- Update from NSA
  * Merged sepol handle passing, seusers support, and policydb cache
    patches from Ivan Gyurdiev.

* Tue Oct 25 2005 Dan Walsh <dwalsh@redhat.com> 1.3.34-1
- Update from NSA
  * Merged resync to sepol changes and booleans fixes/improvements 
    patches from Ivan Gyurdiev.
  * Merged support for genhomedircon/homedir template, store selection,
    explicit policy reload, and semanage.conf relocation from Joshua
    Brindle.

* Mon Oct 24 2005 Dan Walsh <dwalsh@redhat.com> 1.3.32-1
- Update from NSA
  * Merged resync to sepol changes and transaction fix patches from
    Ivan Gyurdiev.
  * Merged reorganize users patch from Ivan Gyurdiev.
  * Merged remove unused relay functions patch from Ivan Gyurdiev.

* Fri Oct 21 2005 Dan Walsh <dwalsh@redhat.com> 1.3.30-1
- Update from NSA
  * Fixed policy file leaks in semanage_load_module and
    semanage_write_module.
  * Merged further database work from Ivan Gyurdiev.
  * Fixed bug in semanage_direct_disconnect.

* Thu Oct 20 2005 Dan Walsh <dwalsh@redhat.com> 1.3.28-1
- Update from NSA
  * Merged interface renaming patch from Ivan Gyurdiev.
  * Merged policy component patch from Ivan Gyurdiev.
  * Renamed 'check=' configuration value to 'expand-check=' for 
    clarity.
  * Changed semanage_commit_sandbox to check for and report errors 
    on rename(2) calls performed during rollback.
  * Added optional check= configuration value to semanage.conf 
    and updated call to sepol_expand_module to pass its value
    to control assertion and hierarchy checking on module expansion.
  * Merged fixes for make DESTDIR= builds from Joshua Brindle.

* Tue Oct 18 2005 Dan Walsh <dwalsh@redhat.com> 1.3.24-1
- Update from NSA
  * Merged default database from Ivan Gyurdiev.
  * Merged removal of connect requirement in policydb backend from
    Ivan Gyurdiev.
  * Merged commit locking fix and lock rename from Joshua Brindle.
  * Merged transaction rollback in lock patch from Joshua Brindle.
  * Changed default args for load_policy to be null, as it no longer
    takes a pathname argument and we want to preserve booleans.
  * Merged move local dbase initialization patch from Ivan Gyurdiev.
  * Merged acquire/release read lock in databases patch from Ivan Gyurdiev.
  * Merged rename direct -> policydb as appropriate patch from Ivan Gyurdiev.
  * Added calls to sepol_policy_file_set_handle interface prior
    to invoking sepol operations on policy files.
  * Updated call to sepol_policydb_from_image to pass the handle.


* Tue Oct 18 2005 Dan Walsh <dwalsh@redhat.com> 1.3.20-1
- Update from NSA
  * Changed default args for load_policy to be null, as it no longer
    takes a pathname argument and we want to preserve booleans.
  * Merged move local dbase initialization patch from Ivan Gyurdiev.
  * Merged acquire/release read lock in databases patch from Ivan Gyurdiev.
  * Merged rename direct -> policydb as appropriate patch from Ivan Gyurdiev.
  * Added calls to sepol_policy_file_set_handle interface prior
    to invoking sepol operations on policy files.
  * Updated call to sepol_policydb_from_image to pass the handle.

* Tue Oct 18 2005 Dan Walsh <dwalsh@redhat.com> 1.3.20-1
- Update from NSA
  * Merged user and port APIs - policy database patch from Ivan
  Gyurdiev.
  * Converted calls to sepol link_packages and expand_module interfaces
  from using buffers to using sepol handles for error reporting, and 
  changed direct_connect/disconnect to create/destroy sepol handles.

* Sat Oct 15 2005 Dan Walsh <dwalsh@redhat.com> 1.3.18-1
- Update from NSA
  * Merged bugfix patch from Ivan Gyurdiev.
  * Merged seuser database patch from Ivan Gyurdiev.
  Merged direct user/port databases to the handle from Ivan Gyurdiev.
  * Removed obsolete include/semanage/commit_api.h (leftover).
  Merged seuser record patch from Ivan Gyurdiev.
  * Merged boolean and interface databases from Ivan Gyurdiev.

* Fri Oct 14 2005 Dan Walsh <dwalsh@redhat.com> 1.3.14-1
- Update from NSA
  * Updated to use get interfaces for hidden sepol_module_package type.
  * Changed semanage_expand_sandbox and semanage_install_active
  to generate/install the latest policy version supported  by libsepol
  by default (unless overridden by semanage.conf), since libselinux
  will now downgrade automatically for load_policy.
  * Merged new callback-based error reporting system and ongoing
  database work from Ivan Gyurdiev.

* Wed Oct 12 2005 Dan Walsh <dwalsh@redhat.com> 1.3.11-1
- Update from NSA
  * Fixed semanage_install_active() to use the same logic for
  selecting a policy version as semanage_expand_sandbox().  Dropped
  dead code from semanage_install_sandbox().

* Mon Oct 10 2005 Dan Walsh <dwalsh@redhat.com> 1.3.10-1
- Update from NSA
  * Updated for changes to libsepol, and to only use types and interfaces
  provided by the shared libsepol.

* Fri Oct 7 2005 Dan Walsh <dwalsh@redhat.com> 1.3.9-1
- Update from NSA
  * Merged further database work from Ivan Gyurdiev.

* Tue Oct 4 2005 Dan Walsh <dwalsh@redhat.com> 1.3.8-1
- Update from NSA
  * Merged iterate, redistribute, and dbase split patches from
  Ivan Gyurdiev.

* Mon Oct 3 2005 Dan Walsh <dwalsh@redhat.com> 1.3.7-1
- Update from NSA
  * Merged patch series from Ivan Gyurdiev.
    (pointer typedef elimination, file renames, dbase work, backend
     separation)
  * Split interfaces from semanage.[hc] into handle.[hc], modules.[hc].
  * Separated handle create from connect interface.
  * Added a constructor for initialization.
  * Moved up src/include/*.h to src.
  * Created a symbol map file; dropped dso.h and hidden markings.

* Wed Sep 28 2005 Dan Walsh <dwalsh@redhat.com> 1.3.5-1
- Update from NSA
  * Split interfaces from semanage.[hc] into handle.[hc], modules.[hc].
  * Separated handle create from connect interface.
  * Added a constructor for initialization.
  * Moved up src/include/*.h to src.
  * Created a symbol map file; dropped dso.h and hidden markings.

* Fri Sep 23 2005 Dan Walsh <dwalsh@redhat.com> 1.3.4-1
- Update from NSA
  * Merged dbase redesign patch from Ivan Gyurdiev.

* Wed Sep 21 2005 Dan Walsh <dwalsh@redhat.com> 1.3.3-1
- Update from NSA
  * Merged boolean record, stub record handler, and status codes 
    patches from Ivan Gyurdiev.

* Tue Sep 20 2005 Dan Walsh <dwalsh@redhat.com> 1.3.2-1
- Update from NSA
  * Merged stub iterator functionality from Ivan Gyurdiev.
  * Merged interface record patch from Ivan Gyurdiev.

* Wed Sep 14 2005 Dan Walsh <dwalsh@redhat.com> 1.3.1-1
- Update from NSA
  * Merged stub functionality for managing user and port records,
  and record table code from Ivan Gyurdiev.
  * Updated version for release.

* Thu Sep 1 2005 Dan Walsh <dwalsh@redhat.com> 1.1.6-1
- Update from NSA
  * Merged semod.conf template patch from Dan Walsh (Red Hat),
  but restored location to /usr/share/semod/semod.conf.
  * Fixed several bugs found by valgrind.
  * Fixed bug in prior patch for the semod_build_module_list leak.
  * Merged errno fix from Joshua Brindle (Tresys).
  * Merged fix for semod_build_modules_list leak on error path
    from Serge Hallyn (IBM).  Bug found by Coverity.

* Thu Aug 25 2005 Dan Walsh <dwalsh@redhat.com> 1.1.3-1
- Update from NSA
  * Merged errno fix from Joshua Brindle (Tresys).
  * Merged fix for semod_build_modules_list leak on error path
    from Serge Hallyn (IBM).  Bug found by Coverity.
  * Merged several fixes from Serge Hallyn (IBM).  Bugs found by
    Coverity.
  * Fixed several other bugs and warnings.
  * Merged patch to move module read/write code from libsemanage
    to libsepol from Jason Tang (Tresys).  
  * Merged relay records patch from Ivan Gyurdiev.
  * Merged key extract patch from Ivan Gyurdiev.

- Initial version
- Created by Stephen Smalley <sds@epoch.ncsc.mil> 


