# -*- coding: utf-8 -*-

# Copyright © 2012-2025 Roberto Alsina and others.

# Permission is hereby granted, free of charge, to any
# person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the
# Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""The default post scanner."""

import glob
import os
import sys

from nikola.global_config import PostConfig, IPostConfig
from nikola.plugin_categories import PostScanner
from nikola import utils
from nikola.post import Post

LOGGER = utils.get_logger('scan_posts')


class ScanPosts(PostScanner):
    """Scan posts in the site."""

    name = "scan_posts"

    def scan(self):
        """Create list of posts from POSTS and PAGES options."""
        if not self.site.quiet:
            print("Scanning posts", end='', file=sys.stderr)
        return self._scan_post(post_config=self.site.config['post_config'])

    def _scan_post(self, post_config: IPostConfig):
        seen = set([])
        timeline = []

        wildcard = post_config.getPattern()
        if not self.site.quiet:
            print(".", end='', file=sys.stderr)
        destination = 'posts'
        template_name = 'post.tmpl'
        use_in_feeds = False
        destination_translatable = utils.TranslatableSetting('destination', destination,
                                                             self.site.config['TRANSLATIONS'])
        dirpath = post_config.getRoot()

        rel_dest_dir = '.'
        # Get all the untranslated paths
        dir_glob = os.path.join(dirpath, os.path.basename(wildcard))  # posts/foo/*.rst
        untranslated = glob.glob(dir_glob)
        full_list = untranslated
        print(f'full_list: {full_list}')
        for base_path in sorted(full_list):
            if base_path in seen:
                continue
            try:
                post = Post(
                    base_path,
                    self.site.config,
                    rel_dest_dir,
                    use_in_feeds,
                    self.site.MESSAGES,
                    template_name,
                    self.site.get_compiler(base_path),
                    destination_base=destination_translatable,
                    metadata_extractors_by=self.site.metadata_extractors_by
                )
                for lang in post.translated_to:
                    seen.add(post.translated_source_path(lang))
                timeline.append(post)
            except Exception:
                LOGGER.error('Error reading post {}'.format(base_path))
                raise

        return timeline

    def supported_extensions(self):
        """Return a list of supported file extensions, or None if such a list isn't known beforehand."""
        return list({os.path.splitext(x[0])[1] for x in self.site.config['post_pages']})
