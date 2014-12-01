from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

# TODO: If you define any fields for the portlet configuration schema below
# do not forget to uncomment the following import
#from zope import schema
from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# TODO: If you require i18n translation for any of your schema fields below,
# uncomment the following to import your package MessageFactory
#from uwosh.secureloginportlet.secureloginportlet import SecureLoginPortletMessageFactory as _

from plone.app.portlets.portlets.login import ILoginPortlet, Assignment as AssignmentBase, Renderer as RendererBase, AddForm as AddFormBase

class ISecureLoginPortlet(ILoginPortlet):
    """A secure login portlet

    It posts to a secure SSL/HTTPS URL for most cases.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    # some_field = schema.TextLine(title=_(u"Some field"),
    #                              description=_(u"A field to use"),
    #                              required=True)


class Assignment(AssignmentBase):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ISecureLoginPortlet)

    # TODO: Set default values for the configurable parameters here

    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u""):
    #    self.some_field = some_field

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Secure Login Portlet"


class Renderer(RendererBase):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    def __init__(self, context, request, view, manager, data):
        RendererBase.__init__(self, context, request, view, manager, data)

        self.uses_plonedev_internal_address = 0
        self.uses_webcluster_internal_address = 0 
        self.uses_localhost_address = 0
        self.uses_internal_address = 0

    def uses_internal_address(self):
        return self.uses_internal_address

    def login_form(self):
        normal_url = '%s/login_form' % self.portal_state.portal_url()
        self.uses_plonedev_internal_address = normal_url.count('http://plonedev.uwosh.edu:') and normal_url.count(':80/') == 0
        self.uses_webcluster_internal_address = normal_url.count('http://plone') and normal_url.count('.webcluster.uwosh.edu:')
        self.uses_localhost_address = normal_url.count('http://localhost:') or normal_url.count('http://127.0.0.1:')
        self.uses_internal_address = self.uses_plonedev_internal_address or self.uses_webcluster_internal_address or self.uses_localhost_address
        return normal_url if self.uses_internal_address else normal_url.replace('http:','https:')

    render = ViewPageTemplateFile('secureloginportlet.pt')


# class AddForm(AddFormBase):
#     """Portlet add form.

#     This is registered in configure.zcml. The form_fields variable tells
#     zope.formlib which fields to display. The create() method actually
#     constructs the assignment that is being added.
#     """
#     form_fields = form.Fields(ISecureLoginPortlet)

#     def create(self, data):
#         return Assignment(**data)


# NOTE: If this portlet does not have any configurable parameters, you
# can use the next AddForm implementation instead of the previous.

class AddForm(base.NullAddForm):
    """Portlet add form.
    """
    def create(self):
        return Assignment()


# NOTE: If this portlet does not have any configurable parameters, you
# can remove the EditForm class definition and delete the editview
# attribute from the <plone:portlet /> registration in configure.zcml


# class EditForm(base.EditForm):
#     """Portlet edit form.

#     This is registered with configure.zcml. The form_fields variable tells
#     zope.formlib which fields to display.
#     """
#     form_fields = form.Fields(ISecureLoginPortlet)
