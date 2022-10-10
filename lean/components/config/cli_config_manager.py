# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean CLI v1.0. Copyright 2021 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional

from lean.components.config.storage import Storage
from lean.constants import DEFAULT_ENGINE_IMAGE, DEFAULT_RESEARCH_IMAGE, DEFAULT_ENGINE_IMAGE_BASE_NAME, \
    DEFAULT_IMAGE_VERSION, DEFAULT_RESEARCH_IMAGE_BASE_NAME
from lean.models.docker import DockerImage
from lean.models.errors import MoreInfoError
from lean.models.options import ChoiceOption, Option


class CLIConfigManager:
    """The CLIConfigManager class contains all configurable CLI options."""

    def __init__(self, general_storage: Storage, credentials_storage: Storage) -> None:
        """Creates a new CLIConfigManager instance.

        :param general_storage: the Storage instance for general, non-sensitive options
        :param credentials_storage: the Storage instance for credentials
        """
        self.user_id = Option("user-id",
                              "The user id used when making authenticated requests to the QuantConnect API.",
                              True,
                              credentials_storage)

        self.api_token = Option("api-token",
                                "The API token used when making authenticated requests to the QuantConnect API.",
                                True,
                                credentials_storage)

        self.default_language = ChoiceOption("default-language",
                                             "The default language used when creating new projects.",
                                             ["python", "csharp"],
                                             False,
                                             general_storage,
                                             "python")

        self.all_options = [
            self.user_id,
            self.api_token,
            self.default_language
        ]

    def get_option_by_key(self, key: str) -> Option:
        """Returns the option matching the given key.

        If no option with the given key exists, an error is raised.

        :param key: the key to look for
        :return: the option having a key equal to the given key
        """
        option = next((x for x in self.all_options if x.key == key), None)

        if option is None:
            raise MoreInfoError(f"There doesn't exist an option with key '{key}'",
                                "https://www.lean.io/docs/v2/lean-cli/api-reference/lean-config-set#02-Description")

        return option

    def get_engine_image_name_from_version(self, version: Optional[str] = None) -> str:
        """Returns the LEAN engine image name to use from the tag.

        :param version: image tag to use
        :return: the image name that should be used when running the LEAN engine
        """
        return self._get_image_name(DEFAULT_ENGINE_IMAGE_BASE_NAME, version)

    def get_engine_image(self, image_name: Optional[str] = None) -> DockerImage:
        """Returns the LEAN engine image to use.

        :param image_name: the image name to use
        :return: the image that should be used when running the LEAN engine
        """
        return self._get_image(image_name, DEFAULT_ENGINE_IMAGE)

    def get_research_image_name_from_version(self, version: Optional[str] = None) -> str:
        """Returns the LEAN research image name to use from the tag.

        :param version: image tag to use
        :return: the image name that should be used when running the research environment
        """
        return self._get_image_name(DEFAULT_RESEARCH_IMAGE_BASE_NAME, version)

    def get_research_image(self, image_name: Optional[str] = None) -> DockerImage:
        """Returns the LEAN research image to use.

        :param image_name: the image name to use
        :return: the image that should be used when running the research environment
        """
        return self._get_image(image_name, DEFAULT_RESEARCH_IMAGE)

    @staticmethod
    def _get_image_name(base_name: str, tag: Optional[str] = None) -> str:
        """Returns the image name given the base name and the tag.

        :param base_name: base name (without tag) of the docker image
        :param tag: the image tag to use
        :return: the image name
        """
        return f"{base_name}:{tag or DEFAULT_IMAGE_VERSION}"

    @staticmethod
    def _get_image(image_name: Optional[str], default_image_name: str) -> DockerImage:
        """Returns the image to use.

        :param option: the CLI option that configures the image type
        :param override: the image name to use, overriding any defaults or previously configured options
        :param default: the default image to use when the option is not set and no override is given
        :return: the image to use
        """
        return DockerImage.parse(image_name or default_image_name)
