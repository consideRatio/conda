# -*- coding: utf-8 -*-
# Copyright (C) 2012 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause

import conda.core.index

from conda.exceptions import PluginError
from conda.base.context import context
from conda.testing.solver_helpers import package_dict
from conda import plugins
from conda.plugins import cuda

import pytest
import re


class VirtualPackagesPlugin:
    @plugins.register
    def conda_virtual_packages(self):
        yield plugins.CondaVirtualPackage(
            name="abc",
            version="123",
        )
        yield plugins.CondaVirtualPackage(
            name="def",
            version="456",
        )
        yield plugins.CondaVirtualPackage(
            name="ghi",
            version="789",
        )


@pytest.fixture()
def plugin(plugin_manager):
    plugin = VirtualPackagesPlugin()
    plugin_manager.register(plugin)
    return plugin


def test_invoked(plugin, cli_main):
    index = conda.core.index.get_reduced_index(
        context.default_prefix,
        context.default_channels,
        context.subdirs,
        (),
        context.repodata_fns[0],
    )

    packages = package_dict(index)

    assert packages["__abc"].version == "123"
    assert packages["__def"].version == "456"
    assert packages["__ghi"].version == "789"


def test_duplicated(plugin_manager, cli_main, capsys):
    plugin_manager.register(VirtualPackagesPlugin())
    plugin_manager.register(VirtualPackagesPlugin())

    with pytest.raises(PluginError, match=re.escape("Conflicting virtual package entries found")):
        conda.core.index.get_reduced_index(
            context.default_prefix,
            context.default_channels,
            context.subdirs,
            (),
            context.repodata_fns[0],
        )


def _clear_cuda_version():
    cuda.cuda_version.cache_clear()


def test_cuda_detection(request):
    # confirm that CUDA detection doesn't raise exception
    request.addfinalizer(_clear_cuda_version)
    version = cuda.cuda_version()
    assert version is None or isinstance(version, str)


def test_cuda_override():
    request.addfinalizer(_clear_cuda_version)
    with env_var('CONDA_OVERRIDE_CUDA', '4.5'):
        version = cuda.cuda_version()
        assert version == '4.5'


def test_cuda_override_none():
    request.addfinalizer(_clear_cuda_version)
    with env_var('CONDA_OVERRIDE_CUDA', ''):
        version = cuda.cuda_version()
        assert version is None
