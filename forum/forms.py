from datetime import datetime

from django import forms
from .models import Category, Post, Forum


# FORUM_ORDER_BY_CHOICES = (
#     ('-last_reply_on', _('Last Reply')),
#     ('-created_on', _('Last Topic')),
# )

# 如果某个topic已经有人发帖可以直接tag

class PostForm(forms.ModelForm):
    # title of the post
    subject = forms.CharField(max_length=500, widget=forms.TextInput(
                                            attrs={'class': 'title',
                                                   'size':'40'}))
    # context of the post
    context = forms.CharField(widget=forms.Textarea(
                                            attrs={'class': 'post_context',
                                                   'rows': '20',
                                                   'cols': '100'}))
    
    class Meta:
        model = Post
        fields = ('subject','context')

    def clean_message(self):
        msg = self.cleaned_data['context']
        forbidden_words = ['fuck','shit','motherfucker']
        for word in forbidden_words:
            word = word.strip()
            if word and word in msg:
                raise forms.ValidationError('Some word in you post is forbidden, please correct it.')
        return msg


class PostFormCategory(forms.ModelForm):
    forum = forms.CharField(max_length=100)
    subject = forms.CharField(max_length=500, widget=forms.TextInput(
                                            attrs={'class': 'title',
                                                   'size':'40'}))
    # context of the post
    context = forms.CharField(widget=forms.Textarea(
                                            attrs={'class': 'post_context',
                                                   'rows': '20',
                                                   'cols': '100'}))
    
    class Meta:
        model = Post
        fields = ('forum', 'subject','context')


# class EditPostForm(PostForm):

#     def __init__(self, *args, **kwargs):
#         instance = kwargs.pop('instance')
#         initial = kwargs.pop('initial', {})
#         initial['subject'] = instance.topic.subject
#         self.forum = instance.topic.forum
#         initial['forum'] = self.forum
#         initial['need_replay'] = instance.topic.need_replay
#         initial['need_reply_attachments'] = instance.topic.need_reply_attachments
#         if instance.topic.topic_type:
#             initial['topic_type'] = instance.topic.topic_type.id
#         super(EditPostForm, self).__init__(*args, instance=instance, initial=initial, **kwargs)
#         if not instance.topic_post:
#             self.fields['subject'].required = False

#     def save(self):
#         post = self.instance
#         post.message = self.cleaned_data['message']
#         post.updated_on = datetime.now()
#         post.edited_by = self.user.lbforum_profile.nickname
#         attachments = self.cleaned_data['attachments']
#         post.update_attachments(attachments)
#         post.save()
#         if post.topic_post:
#             topic = post.topic
#             topic.forum = self.forum
#             topic.subject = self.cleaned_data['subject']
#             topic.need_replay = self.cleaned_data['need_replay']
#             topic.need_reply_attachments = self.cleaned_data['need_reply_attachments']
#             topic_type = self.cleaned_data['topic_type']
#             if topic_type:
#                 topic_type = TopicType.objects.get(id=topic_type)
#             else:
#                 topic_type = None
#             topic.topic_type = topic_type
#             topic.save()
#         return post
# category = forms.ModelChoiceField(queryset= Category.objects.all())
# # topic
#     forum = forms.CharField(max_length=500, widget=forms.TextInput(
#                                             attrs={'class': 'forum',
#                                                    'size':'40'}))





